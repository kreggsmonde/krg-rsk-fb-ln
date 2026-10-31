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
  },
  {
    "episode": 3,
    "topic": "Искусство быть собой рядом с любимым",
    "date": "2026-10-29T08:17:19.575223",
    "duration_sec": 1375.21,
    "duration_min": 22.92,
    "video_file": "podcast_ep3_20261029_075637.mp4",
    "thumbnail_file": "thumb_ep3_20261029_075637.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 4,
    "topic": "Искусство доверять, когда страшно",
    "date": "2026-10-30T08:12:08.366235",
    "duration_sec": 1328.75,
    "duration_min": 22.15,
    "video_file": "podcast_ep4_20261030_075908.mp4",
    "thumbnail_file": "thumb_ep4_20261030_075908.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 5,
    "topic": "Искусство благодарить: как сделать комплимент по-настоящему ценным",
    "date": "2026-10-31T08:08:48.395945",
    "duration_sec": 1378.91,
    "duration_min": 22.98,
    "video_file": "podcast_ep5_20261031_075442.mp4",
    "thumbnail_file": "thumb_ep5_20261031_075442.jpg",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
