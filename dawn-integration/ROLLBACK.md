# DAWN AutoClip rollback boundary

## Current repository-only state

The branch adds contracts, fixtures and an offline validator only. It does not install AutoClip, process media, start a server or write output assets.

Rollback is to close the draft PR and delete the branch.

## Future Mac canary rollback

A later media canary must:

1. stop the foreground AutoClip process and verify its process tree is gone;
2. remove only the isolated environment, canary work directory and generated clips;
3. unset or remove any temporary local configuration created for the canary;
4. confirm no social account, cloud provider or credential was accessed;
5. confirm no approved asset bank, Postiz queue, Qdrant, Hindsight or Obsidian record changed;
6. retain commands, checksums, resource measurements and visual-review findings.

No automatic retry may switch from local Ollama to a cloud provider, download media or publish an asset.