from moviepy.editor import *
import os

def Split_Video_files(path_to_videos,target_folder,time):
    '''listing individual files and forwarding it to split anc converting to .wav file'''
	path_to_videos= path_to_videos 
	
	target_folder = target_folder                       #saving splited videos
	if not os.path.exists(target_folder):
		os.makedirs(target_folder) 
	video_files=[]
	
	time=time #second of split
	for files in os.listdir(path_to_videos):
		if files.endswith(".mp4"):
			video_files.append(path_to_videos+'/'+files)

	for files in video_files:
		Convert(files,target_folder,time) # converting splitted videos to wav


def Convert(input_file,target_folder,split_seconds):
   '''splits video file and convert splitted video file to .wav format'''
	
	video =  VideoFileClip(input_file) 
	video_length = video.duration           #length of video file

	i=0
	cur_length=split_seconds 
	duration=split_seconds                 
	filename=input_file.split('/')[-1][:-4]
	
	while True:
		if i+duration>video_length: # for last split when length video left for splitting < split seconds
			video1 = video.subclip(i,video_length)
			result = CompositeVideoClip([video1])
			name=target_folder+"/"+filename+"_"+str(i)+' - '+str(video_length)+'.mp4' # saving splitted video to target folder
			result.write_videofile(name,codec='mpeg4',bitrate='20000k')
			result.audio.write_audiofile(target_folder+"/"+filename+"_"+str(i)+' - '+str(cur_length)+".wav",fps=44100,bitrate="20000k") #convert to wav
			break
		video1 = video.subclip(i,cur_length)
		result = CompositeVideoClip([video1])
		#name=str(i)+' - '+str(cur_length)+'.mp4'
		name=target_folder+"/"+filename+"_"+str(i)+' - '+str(cur_length)+'.mp4'
		result.write_videofile(name,codec='mpeg4',bitrate='20000k')
		result.audio.write_audiofile(target_folder+"/"+filename+"_"+str(i)+' - '+str(cur_length)+".wav",fps=44100,bitrate="20000k")
		i=cur_length
		cur_length=cur_length+duration






