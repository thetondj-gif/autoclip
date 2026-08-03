# DAWN AutoClip — Capability Foundry Wave 2

## Status

`CAPABILITY_PREPARATION_READY`

This package prepares AutoClip as an isolated local media executor. It does not install AutoClip, process media, contact a provider, start its web service, access a social account or connect it to live DAWN.

## Intended first canary

Use one short, operator-owned local video file and a local Ollama model to produce no more than three reviewable 9:16 clip candidates in a dedicated canary output directory.

## Required controls

- source media must be owned or explicitly licensed;
- local-file input only for the first canary;
- no YouTube or remote download;
- no cloud provider or API credential;
- no diarisation model download;
- no direct publishing or social credentials;
- bounded source duration, clip count and output directory;
- before/after CPU, memory, disk, process and port evidence;
- visual review before any asset enters the approved image/video bank.

## First acceptance slice

`acceptance.py` validates a proposed canary request using synthetic JSON fixtures. It deliberately performs no file read, transcription, rendering, network request or model call.

## Connection gate

AutoClip may advance to a Mac-local media canary only after this offline boundary passes, `autoclip doctor` is reviewed, the exact ffmpeg build is proven to include `libass` and `libx264`, and a separate operator approval identifies the source file and output directory.
