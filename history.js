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
  },
  {
    "episode": 6,
    "topic": "Искусство близости: как сохранить интимность в долгосрочных отношениях",
    "date": "2026-11-01T08:58:47.025517",
    "duration_sec": 1397.17,
    "duration_min": 23.29,
    "video_file": "podcast_ep6_20261101_083725.mp4",
    "thumbnail_file": "thumb_ep6_20261101_083725.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 7,
    "topic": "Искусство строить мосты после шторма: как примиряться, не теряя себя",
    "date": "2026-11-02T09:05:04.441911",
    "duration_sec": 1463.46,
    "duration_min": 24.39,
    "video_file": "podcast_ep7_20261102_084639.mp4",
    "thumbnail_file": "thumb_ep7_20261102_084639.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 8,
    "topic": "Искусство просить о нежности: как говорить, чтобы слышали",
    "date": "2026-11-03T09:19:36.442315",
    "duration_sec": 1375.79,
    "duration_min": 22.93,
    "video_file": "podcast_ep8_20261103_085657.mp4",
    "thumbnail_file": "thumb_ep8_20261103_085657.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 9,
    "topic": "Искусство отпускать обиды: возвращать близость без наказаний",
    "date": "2026-11-04T08:50:19.730573",
    "duration_sec": 1367.29,
    "duration_min": 22.79,
    "video_file": "podcast_ep9_20261104_082917.mp4",
    "thumbnail_file": "thumb_ep9_20261104_082917.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 10,
    "topic": "Искусство тёплых разговоров: как обсуждать сложное без холодной защиты",
    "date": "2026-11-05T09:14:38.062670",
    "duration_sec": 1400.36,
    "duration_min": 23.34,
    "video_file": "podcast_ep10_20261105_085338.mp4",
    "thumbnail_file": "thumb_ep10_20261105_085338.jpg",
    "platform": "Facebook"
  },
  {
    "episode": 11,
    "topic": "Искусство успокаивать друг друга: как снижать тревогу, а не раздувать её",
    "date": "2026-11-06T09:06:12.304948",
    "duration_sec": 1378.74,
    "duration_min": 22.98,
    "video_file": "podcast_ep11_20261106_085241.mp4",
    "thumbnail_file": "thumb_ep11_20261106_085241.jpg",
    "platform": "Facebook"
  }
];
if (typeof module !== 'undefined' && module.exports) { module.exports = PODCAST_HISTORY; }
if (typeof window !== 'undefined') { window.PODCAST_HISTORY = PODCAST_HISTORY; }
