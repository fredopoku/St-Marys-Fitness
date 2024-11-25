"""
Base repository providing common CRUD operations for other repositories.
"""

import json
import os
from typing import Generic, TypeVar, List, Optional
from src.models.common import BaseModel

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    """A base repository for common CRUD operations"""

    def __init__(self, file_path: str):
        """
        Initialize the repository with a file path for data persistence.

        :param file_path: Path to the JSON file for storage.
        """
        self.file_path = file_path
        self.data: List[T] = []
        self._load()

    def _load(self):
        """Load data from the JSON file if it exists."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    raw_data = json.load(file)
                    self.data = [self._deserialize(item) for item in raw_data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data from {self.file_path}: {e}")

    def _save(self):
        """Save data to the JSON file."""
        try:
            with open(self.file_path, 'w') as file:
                raw_data = [item.to_dict() for item in self.data]
                json.dump(raw_data, file, indent=4)
        except IOError as e:
            print(f"Error saving data to {self.file_path}: {e}")

    def _deserialize(self, raw_data: dict) -> T:
        """
        Convert a dictionary back into the model.

        :param raw_data: Raw dictionary data from the file.
        :return: Deserialized model instance.
        """
        return T.from_dict(raw_data)

    def add(self, item: T) -> T:
        """
        Add a new item to the repository.

        :param item: The item to add.
        :return: The added item.
        """
        self.data.append(item)
        self._save()
        return item

    def get_all(self) -> List[T]:
        """
        Get all items in the repository.

        :return: A list of all items.
        """
        return self.data

    def get_by_id(self, item_id: str) -> Optional[T]:
        """
        Retrieve an item by its unique ID.

        :param item_id: The ID of the item.
        :return: The item if found, None otherwise.
        """
        return next((item for item in self.data if item.id == item_id), None)

    def update(self, item: T) -> bool:
        """
        Update an existing item.

        :param item: The item to update.
        :return: True if updated successfully, False otherwise.
        """
        for index, existing_item in enumerate(self.data):
            if existing_item.id == item.id:
                self.data[index] = item
                self._save()
                return True
        return False

    def delete(self, item_id: str) -> bool:
        """
        Delete an item by its ID.

        :param item_id: The ID of the item to delete.
        :return: True if deleted successfully, False otherwise.
        """
        initial_length = len(self.data)
        self.data = [item for item in self.data if item.id != item_id]
        if len(self.data) < initial_length:
            self._save()
            return True
        return False
