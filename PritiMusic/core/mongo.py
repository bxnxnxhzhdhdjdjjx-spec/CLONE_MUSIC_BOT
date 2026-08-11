import os
import json
import asyncio
from typing import Any, Dict, List, Optional

from ..logging import LOGGER

LOGGER(__name__).info("Initializing local JSON-based database...")

JSON_DB_DIR = "json_db"
os.makedirs(JSON_DB_DIR, exist_ok=True)


def _match_document(doc: Dict[str, Any], filter_dict: Optional[Dict[str, Any]]) -> bool:
    if not filter_dict:
        return True
    for key, val in filter_dict.items():
        if key not in doc:
            # If checking if field doesn't exist
            if isinstance(val, dict) and "$exists" in val and not val["$exists"]:
                continue
            return False

        doc_val = doc[key]
        if isinstance(val, dict):
            for op, op_val in val.items():
                if op == "$gt":
                    if not (isinstance(doc_val, (int, float)) and isinstance(op_val, (int, float)) and doc_val > op_val):
                        return False
                elif op == "$lt":
                    if not (isinstance(doc_val, (int, float)) and isinstance(op_val, (int, float)) and doc_val < op_val):
                        return False
                elif op == "$gte":
                    if not (isinstance(doc_val, (int, float)) and isinstance(op_val, (int, float)) and doc_val >= op_val):
                        return False
                elif op == "$lte":
                    if not (isinstance(doc_val, (int, float)) and isinstance(op_val, (int, float)) and doc_val <= op_val):
                        return False
                elif op == "$exists":
                    if bool(op_val) != True: # key already exists, but val expects it not to
                        return False
                elif op == "$in":
                    if not isinstance(op_val, list) or doc_val not in op_val:
                        return False
                elif op == "$nin":
                    if not isinstance(op_val, list) or doc_val in op_val:
                        return False
                else:
                    if doc_val != val:
                        return False
        else:
            if doc_val != val:
                return False
    return True


def _update_document(doc: Dict[str, Any], update_dict: Dict[str, Any]) -> Dict[str, Any]:
    if "$set" in update_dict:
        for k, v in update_dict["$set"].items():
            doc[k] = v
    if "$unset" in update_dict:
        for k in update_dict["$unset"].keys():
            doc.pop(k, None)
    return doc


class JSONCursor:
    def __init__(self, collection: "JSONCollection", filter_dict: Optional[Dict[str, Any]] = None):
        self.collection = collection
        self.filter_dict = filter_dict
        self._index = 0
        self._matched_data: Optional[List[Dict[str, Any]]] = None

    async def _ensure_matched(self):
        if self._matched_data is None:
            await self.collection._load()
            self._matched_data = [
                doc for doc in self.collection._data
                if _match_document(doc, self.filter_dict)
            ]

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self._ensure_matched()
        if self._index >= len(self._matched_data):
            raise StopAsyncIteration
        val = self._matched_data[self._index]
        self._index += 1
        return val

    async def to_list(self, length: int = 100000) -> List[Dict[str, Any]]:
        await self._ensure_matched()
        return self._matched_data[:length]


class JSONCollection:
    def __init__(self, db_name: str, collection_name: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.file_path = os.path.join(JSON_DB_DIR, f"{db_name}_{collection_name}.json")
        self.lock = asyncio.Lock()
        self._data: List[Dict[str, Any]] = []
        self._loaded = False

    async def _load(self):
        if self._loaded:
            return
        async with self.lock:
            if self._loaded:
                return
            os.makedirs(JSON_DB_DIR, exist_ok=True)
            if os.path.exists(self.file_path):
                try:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        self._data = json.load(f)
                except Exception:
                    self._data = []
            else:
                self._data = []
            self._loaded = True

    async def _save(self):
        async with self.lock:
            os.makedirs(JSON_DB_DIR, exist_ok=True)
            temp_path = self.file_path + ".tmp"
            try:
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(self._data, f, indent=4, ensure_ascii=False)
                os.replace(temp_path, self.file_path)
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise e

    async def find_one(self, filter_dict: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        await self._load()
        for doc in self._data:
            if _match_document(doc, filter_dict):
                return doc
        return None

    def find(self, filter_dict: Optional[Dict[str, Any]] = None) -> JSONCursor:
        return JSONCursor(self, filter_dict)

    async def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False):
        await self._load()
        found = False
        for doc in self._data:
            if _match_document(doc, filter_dict):
                _update_document(doc, update_dict)
                found = True
                break
        if not found and upsert:
            new_doc = dict(filter_dict)
            for k, v in list(new_doc.items()):
                if isinstance(v, dict):
                    new_doc.pop(k, None)
            _update_document(new_doc, update_dict)
            self._data.append(new_doc)
        await self._save()

    async def insert_one(self, document: Dict[str, Any]):
        await self._load()
        self._data.append(document)
        await self._save()

    async def delete_one(self, filter_dict: Dict[str, Any]):
        await self._load()
        for i, doc in enumerate(self._data):
            if _match_document(doc, filter_dict):
                self._data.pop(i)
                break
        await self._save()

    async def count_documents(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        await self._load()
        if not filter_dict:
            return len(self._data)
        count = 0
        for doc in self._data:
            if _match_document(doc, filter_dict):
                count += 1
        return count

    async def delete_many(self, filter_dict: Optional[Dict[str, Any]] = None):
        await self._load()
        if not filter_dict:
            self._data = []
        else:
            self._data = [doc for doc in self._data if not _match_document(doc, filter_dict)]
        await self._save()


class MockMongoDatabase:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.collections: Dict[str, JSONCollection] = {}

    def __getattr__(self, name: str) -> JSONCollection:
        if name not in self.collections:
            self.collections[name] = JSONCollection(self.db_name, name)
        return self.collections[name]

    def __getitem__(self, name: str) -> JSONCollection:
        return self.__getattr__(name)

    async def command(self, cmd_name: str) -> Dict[str, Any]:
        if cmd_name == "dbstats":
            num_collections = 0
            num_objects = 0
            total_size = 0
            os.makedirs(JSON_DB_DIR, exist_ok=True)
            for file_name in os.listdir(JSON_DB_DIR):
                if file_name.startswith(f"{self.db_name}_") and file_name.endswith(".json"):
                    num_collections += 1
                    try:
                        file_path = os.path.join(JSON_DB_DIR, file_name)
                        total_size += os.path.getsize(file_path)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            num_objects += len(data)
                    except Exception:
                        pass
            return {
                "dataSize": total_size or 1024,
                "storageSize": total_size or 1024,
                "collections": num_collections or 1,
                "objects": num_objects or 1
            }
        return {}


# Expose mongodb and pymongodb to the rest of the application
mongodb = MockMongoDatabase("Anon")
pymongodb = mongodb
