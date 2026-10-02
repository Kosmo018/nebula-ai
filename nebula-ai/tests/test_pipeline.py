"""Pipeline tests for Nebula AI."""

from unittest.mock import MagicMock, patch

from src.main import PROJECT_DIR, VIDEO_URL, download_video


def test_download_video_runs_ytdlp() -> None:
    with patch("src.main.subprocess.run") as run:
        run.return_value = MagicMock(returncode=0)
        download_video(VIDEO_URL)

    run.assert_called_once()
    args = run.call_args.args[0]
    assert args[0] == "yt-dlp"
    assert VIDEO_URL in args
    assert str(PROJECT_DIR / "%(title)s.%(ext)s") in args
    assert run.call_args.kwargs["check"] is True
