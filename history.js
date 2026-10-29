// История выпусков и реестр тем
const PODCAST_HISTORY = [
  {
    "episode": 1,
    "topic": "Искусство слушать друг друга в паре",
    "date": "2026-10-26T05:29:08.843989",
    "duration_sec": 179.41,
    "duration_min": 2.99,
    "video_file": "podcast_ep1_20261026_052731.mp4",
    "thumbnail_file": "thumb_ep1_20261026_052731.jpg",
    "platform": "Local"
  },
  {
    "episode": 2,
    "topic": "Искусство говорить 'нет' ради любви",
    "date": "2026-10-29T02:43:05.197635",
    "duration_sec": 173.38,
    "duration_min": 2.89,
    "video_file": "podcast_ep2_20261029_024153.mp4",
    "thumbnail_file": "thumb_ep2_20261029_024153.jpg",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
