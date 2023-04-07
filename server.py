import argparse
import os
import libtorrent as lt 
from env import EnvironmentSettings
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from aiohttp import ClientSession
import logging
from typing import Optional, Dict, Union
from models import TorrentStats
from utils import Utils

MAX_READ_BYTES = 100 * 1024 * 1024 #100mB

# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TorrentFlow-logger')

app = FastAPI()
utils = Utils()

env_settings = EnvironmentSettings()
ses = lt.session(env_settings.get_lt_settings_dict())

async def handle_torrent_url(torrent_url, save_path):
    if save_path:
        os.makedirs(save_path, exist_ok=True)

    if not torrent_url:
        logger.warning("handle_torrent_url: got called with torrent_url=None")
        raise Exception("torrent_url cannot be None")

    if utils.is_magnet(torrent_url):
        logger.info(f"handle_torrent_url: {torrent_url} is magnet")
        parsed = lt.parse_magnet_uri(torrent_url)
        parsed.save_path = save_path if save_path else '.'
        return parsed
    else:
        async with ClientSession() as session:
            async with session.get(torrent_url) as response:
                logger.info(f"handle_torrent_url: {response.status} | {response.content_type} | {response.content_length}")
                if response.status >= 400:
                    raise Exception(f"{torrent_url} returned http statusCode={response.status}")
                if "bittorrent" not in response.content_type:
                    raise Exception(f"{torrent_url} returned a resource that does not have content-type as bittorrent")
                if response.content_length > MAX_READ_BYTES:
                    raise Exception(f"{torrent_url} content-length exceeds the limit")
                data = await response.content.read()
                info = lt.torrent_info(lt.bdecode(data))
                parsed = {
                    'ti': info,
                    'save_path': save_path if save_path else '.',
                    'info_hash': info.info_hash() 
                }
                return parsed

@app.post("/torrents", response_model=Dict[str, str])
async def add_torrent(torrent_url: Optional[str] = Form(None), save_path: Optional[str] = Form(None), torrent_file: Union[UploadFile, None] = None):
    lt_add_torrent_params = None 
    if torrent_url:
        try:
            lt_add_torrent_params = await handle_torrent_url(torrent_url, save_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif torrent_file:
        info = lt.torrent_info(lt.bdecode(await torrent_file.read()))
        lt_add_torrent_params = {
            'ti': info,
            'save_path': save_path if save_path else '.',
            'info_hash': info.info_hash() 
        }
    else:
        raise HTTPException(status_code=400, detail="Either torrent_url or torrent_file must be provided")

    try:
        infohash = str(lt_add_torrent_params.info_hash)
    except AttributeError:
        infohash = str(lt_add_torrent_params['info_hash'])
        del lt_add_torrent_params['info_hash']

    ses.async_add_torrent(lt_add_torrent_params)
    return {
        'info_hash': infohash
    }

@app.delete("/torrents/{infohash}")
async def remove_torrent(infohash: str):
    torrent_handle = None
    for handle in ses.get_torrents():
        if str(handle.info_hash()) == infohash:
            torrent_handle = handle
            break

    if not torrent_handle:
        raise HTTPException(status_code=404, detail="Torrent not found")

    ses.remove_torrent(torrent_handle)
    return {"result": "Torrent removed"}

@app.put("/torrents/{infohash}/pause")
async def pause_torrent(infohash: str):
    torrent_handle = None
    for handle in ses.get_torrents():
        if str(handle.info_hash()) == infohash:
            torrent_handle = handle
            break

    if not torrent_handle:
        raise HTTPException(status_code=404, detail="Torrent not found")

    torrent_handle.pause()
    return {"result": "Torrent paused"}

@app.put("/torrents/{infohash}/resume")
async def resume_torrent(infohash: str):
    torrent_handle = None
    for handle in ses.get_torrents():
        if str(handle.info_hash()) == infohash:
            torrent_handle = handle
            break

    if not torrent_handle:
        raise HTTPException(status_code=404, detail="Torrent not found")

    torrent_handle.resume()
    return {"result": "Torrent resumed"}


@app.get("/torrents/{infohash}", response_model=TorrentStats)
async def get_torrent_stats(infohash: str):
    torrent_handle = None
    for handle in ses.get_torrents():
        if str(handle.info_hash()) == infohash:
            torrent_handle = handle
            break

    if not torrent_handle:
        raise HTTPException(status_code=404, detail="Torrent not found")
    torrent_status = torrent_handle.status()
    torrent_info = torrent_handle.torrent_file()
    torrent_status_dict = {
        'infohash': infohash,
        'state': str(torrent_status.state),
        'paused': torrent_status.paused,
        'auto_managed': torrent_status.auto_managed,
        'sequential_download': torrent_status.sequential_download,
        'is_seeding': torrent_status.is_seeding,
        'is_finished': torrent_status.is_finished,
        'has_metadata': torrent_status.has_metadata,
        'progress': torrent_status.progress * 100,
        'error': torrent_status.error,
        'download_rate': torrent_status.download_rate,
        'upload_rate': torrent_status.upload_rate,
        'total_download': torrent_status.total_download,
        'total_upload': torrent_status.total_upload,
        'num_peers': torrent_status.num_peers,
        'list_peers': torrent_status.list_peers,
        'list_seeds': torrent_status.list_seeds,
        'connect_candidates': torrent_status.connect_candidates,
        'num_pieces': torrent_status.num_pieces,
        'total_done': torrent_status.total_done,
        'total_wanted_done': torrent_status.total_wanted_done,
        'total_wanted': torrent_status.total_wanted,
        'distributed_copies': torrent_status.distributed_copies,
        'num_seeds': torrent_status.num_seeds,
        'num_complete': torrent_status.num_complete,
        'num_incomplete': torrent_status.num_incomplete,
        'last_seen_complete': torrent_status.last_seen_complete,
        'time_since_upload': torrent_status.time_since_upload,
        'time_since_download': torrent_status.time_since_download,
        'active_time': torrent_status.active_time,
        'finished_time': torrent_status.finished_time,
        'seeding_time': torrent_status.seeding_time,
        'seed_rank': torrent_status.seed_rank,
        'last_scrape': torrent_status.last_scrape,
        'has_incoming': torrent_status.has_incoming,
        'seed_mode': torrent_status.seed_mode,
        'upload_mode': torrent_status.upload_mode,
        'share_mode': torrent_status.share_mode,
        'super_seeding': torrent_status.super_seeding,
        'priority': torrent_status.priority,
        'added_time': torrent_status.added_time,
        'completed_time': torrent_status.completed_time,
        'storage_mode': str(torrent_status.storage_mode),
        'save_path': torrent_status.save_path,
        'name': torrent_info.name(),
        'total_size': torrent_info.total_size(),
        'num_files': torrent_info.num_files(),
        'creation_date': torrent_info.creation_date(),
        'creator': torrent_info.creator(),
        'comment': torrent_info.comment(),
        'piece_length': torrent_info.piece_length(),
        'num_pieces': torrent_info.num_pieces(),
        'total_pieces': torrent_handle.torrent_file().num_pieces() if torrent_handle.torrent_file() else 0,
        'files': [
            {
                'path': file_entry.path,
                'size': file_entry.size,
                'offset': file_entry.offset,
            }
            for file_entry in torrent_info.files()
        ],
    }
    return torrent_status_dict
