from loguru import logger
from typing import BinaryIO
from app.config import FMConfig
from aiofiles import open
from os.path import join, dirname, isdir, isfile
from os import makedirs, remove


class FileManager:
    def __init__(self, config: dict | FMConfig) -> None:
        logger.info('File manager initialization...')

        self._config: FMConfig = config if type(config) is FMConfig else FMConfig(config)
        self._dir = self._config.DIR

    async def save(self, path: str, file_io: BinaryIO) -> None:
        path = join(self._dir, path)
        self.mkdir(dirname(path))
        
        logger.info(f'Save file: {path}')

        async with open(path, mode='wb') as file:
            await file.write(file_io.read())

    def delete(self, path: str):
        path = join(self._dir, path)
        
        if isfile(path):
            logger.info(f'Delete file: {path}')
            remove(path)

    async def get(self, path: str) -> bytes:
        path = join(self._dir, path)
        async with open(path, mode='rb') as file:
            return await file.read()

    def mkdir(self, path) -> None:
        if not isdir(path):
            logger.info(f'Create directory: {path}')
            makedirs(path, exist_ok=True)
