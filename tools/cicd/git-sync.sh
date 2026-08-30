#!/usr/bin/env bash
#
# Poll a remote branch; if it moved, sync to it and run a callback.
#
#   git-sync.sh <repo-dir> <branch> [callback]
#
# The local branch is made to match the remote exactly. A clean
# fast-forward is preferred; if the branch has diverged or been
# force-pushed, local history is discarded via reset --hard.
#
# callback defaults to "on-update.sh"; relative paths are resolved
# inside the repo. It is invoked as: callback <old-sha> <new-sha>
# Exit 0 = nothing to do or updated successfully.

set -euo pipefail

usage() {
    echo "usage: $(basename "$0") <repo-dir> <branch> [callback]" >&2
    exit 2
}

die() {
    echo "$(basename "$0"): $*" >&2
    exit 1
}

[ $# -ge 2 ] && [ $# -le 3 ] || usage

repo=$1
branch=$2
callback=${3:-on-update.sh}

[ -d "$repo" ] || die "no such directory: $repo"
cd "$repo"
git rev-parse --git-dir >/dev/null 2>&1 || die "not a git repository: $repo"

# resolve a relative callback against the repo root
case "$callback" in
    /*) ;;
    *) callback="$PWD/$callback" ;;
esac

# refuse to touch anything if we are not actually sitting on that branch
current=$(git symbolic-ref --short -q HEAD || true)
[ "$current" = "$branch" ] || die "HEAD is on '${current:-detached}', expected '$branch'"

# cheap check: reads the remote's ref list only, downloads no objects
remote_sha=$(git ls-remote --exit-code origin "refs/heads/$branch" | cut -f1) \
    || die "branch '$branch' not found on origin"
local_sha=$(git rev-parse HEAD)

[ "$remote_sha" = "$local_sha" ] && exit 0

echo "$branch: ${local_sha:0:8} -> ${remote_sha:0:8}"
git fetch origin "$branch"

# fast-forward if we can, otherwise take the remote wholesale
if git merge-base --is-ancestor "$local_sha" "$remote_sha" 2>/dev/null; then
    if ! git merge --ff-only "$remote_sha"; then
        echo "fast-forward blocked by local changes, resetting" >&2
        git reset --hard "$remote_sha"
    fi
else
    ahead=$(git rev-list --count "$remote_sha..$local_sha" 2>/dev/null || echo "?")
    echo "diverged: discarding $ahead local commit(s), reflog keeps ${local_sha:0:8}" >&2
    git reset --hard "$remote_sha"
fi

if [ -x "$callback" ]; then
    "$callback" "$local_sha" "$remote_sha"
else
    echo "callback not executable, skipping: $callback" >&2
fi
