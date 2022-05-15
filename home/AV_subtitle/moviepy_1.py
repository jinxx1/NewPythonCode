from moviepy.editor import VideoClip, concatenate_videoclips,VideoFileClip
import os

if __name__ == '__main__':
	basePath = "D:\BT_download\[7sht.me]ABP-601A-C无码流出"
	v1FileName = "ABP-601A-C.mp4"
	v2FileName = "ABP-601B-C.mp4"
	v1Path = os.path.join(basePath, v1FileName)
	v2Path = os.path.join(basePath, v2FileName)

	v1 = VideoFileClip(v1Path)
	v2 = VideoFileClip(v2Path)

	vinal_v = concatenate_videoclips([v1, v2])
	vinal_v.write_videofile(os.path.join(basePath, "ABP-601中文字幕无码流出.mp4"))

