import subprocess

async def check_chat(update, chat):
    # Code to check chat type
    pass

async def encode_video(input_file, settings):
    output_file = f"encoded_{input_file}"
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',
        '-crf', settings['crf'],
        '-preset', settings['preset'],
        '-s', f"{settings['resolution']}p",
        output_file
    ]
    
    subprocess.run(command)
    
    return output_file

output = None  # Define output if needed
