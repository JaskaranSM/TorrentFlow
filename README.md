# TorrentFlow

TorrentFlow is a simple and efficient microservice for managing torrent downloads and providing torrent-related statistics through an easy-to-use API. It is built using Python, FastAPI, and the libtorrent library.

## Features

- Add torrents via URL or file upload
- Remove torrents using infohash
- Get torrent status and statistics
- Pause and resume torrents
- Customizable save paths for downloaded torrents

## Endpoints

### POST /torrents

Add a torrent via URL or file upload.

**Request**

- `torrent_url` (form field): The URL or magnet link of the torrent. Either this field or `torrent_file` must be provided.
- `torrent_file` (form field, optional): The .torrent file to be uploaded. Either this field or `torrent_url` must be provided.
- `save_path` (form field, optional): The custom save path for the torrent.

**Response**

- `infohash`: The infohash of the added torrent.

### DELETE /torrents/{infohash}

Remove a torrent using its infohash.

**Path Parameters**

- `infohash`: The infohash of the torrent to remove.

**Response**

- `detail`: A description of the operation result.

### GET /torrents/{infohash}

Get the status of a torrent using its infohash.

**Path Parameters**

- `infohash`: The infohash of the torrent to get the status for.

**Response**

- `infohash`: The infohash of the torrent.
- `state`: The current state of the torrent.
- `paused`: Whether the torrent is paused.
- `auto_managed`: Whether the torrent is auto-managed.
- `sequential_download`: Whether the torrent is using sequential download.
- `is_seeding`: Whether the torrent is seeding.
- `is_finished`: Whether the torrent is finished.
- `has_metadata`: Whether the torrent has metadata.
- `progress`: The progress of the torrent download as a percentage.
- `error`: Any error message associated with the torrent.
- `download_rate`: The download rate of the torrent in bytes per second.
- `upload_rate`: The upload rate of the torrent in bytes per second.
- `total_download`: The total amount downloaded for the torrent in bytes.
- `total_upload`: The total amount uploaded for the torrent in bytes.
- `num_peers`: The number of peers connected to the torrent.
- `list_peers`: The number of listed peers.
- `list_seeds`: The number of listed seeds.
- `connect_candidates`: The number of connection candidates.
- `num_pieces`: The number of downloaded pieces.
- `total_pieces`: The total number of pieces for the torrent.
- `total_done`: The total amount of completed data in bytes.
- `total_wanted_done`: The total amount of wanted data that is completed in bytes.
- `total_wanted`: The total amount of wanted data in bytes.
- `distributed_copies`: The number of distributed copies.
- `num_seeds`: The number of seeds connected to the torrent.
- `num_complete`: The number of completed peers.
- `num_incomplete`: The number of incomplete peers.
- `last_seen_complete`: The last time a complete peer was seen.
- `time_since_upload`: The time since the last upload in seconds.
- `time_since_download`: The time since the last download in seconds.
- `active_time`: The active time of the torrent in seconds.
- `finished_time`: The finished time of the torrent in seconds.
- `seeding_time`: The seeding time of the torrent in seconds.
- `seed_rank`: The seed rank of the torrent.
- `last_scrape`: The time since the last scrape in seconds.
- `has_incoming`: Whether the torrent has incoming connections.
- `seed_mode`: Whether the torrent is in seed mode.
- `upload_mode`: Whether the torrent is in upload mode.
- `share_mode`: Whether the torrent is in share mode.
- `super_seeding`: Whether the torrent is in super seeding mode.
- `priority`: The priority of the torrent.
- `added_time`: The time when the torrent was added in seconds.
- `completed_time`: The time when the torrent was completed in seconds.
- `storage_mode`: The storage mode of the torrent.
- `save_path`: The save path of the torrent.
- `name`: The name of the torrent.
- `total_size`: The total size of the torrent in bytes.
- `num_files`: The number of files in the torrent.
- `creation_date`: The creation date of the torrent in seconds.
- `creator`: The creator of the torrent.
- `comment`: The comment of the torrent.
- `piece_length`: The length of each piece in bytes.
- `num_pieces`: The total number of pieces in the torrent.
- `files`: The list of files in the torrent.

### PUT /torrents/{infohash}/pause

Pause a torrent using its infohash.

**Path Parameters**

- `infohash`: The infohash of the torrent to pause.

**Response**

- `detail`: A description of the operation result.

### PUT /torrents/{infohash}/resume

Resume a paused torrent using its infohash.

**Path Parameters**

- `infohash`: The infohash of the torrent to resume.

**Response**

- `detail`: A description of the operation result.

## Installation and Usage

Please refer to the provided `Dockerfile` for building and running TorrentFlow
