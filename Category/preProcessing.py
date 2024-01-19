import pandas as pd
import cv2

def pre_processing(df, cap):
    df = df[['frame_number', 'category']]
    # categories = df['category'].unique()
    category_col = 'category'
    frame_number_col = 'frame_number'

    # Find the indices where the category is not in numerical order
    index_after_5 = df[df[category_col] == 5].index.max()

    # Keep all rows that come after the index with category 5
    df_before_and_at_5 = df.loc[:index_after_5].reset_index(drop=True)
    category_ranges = df_before_and_at_5.groupby(category_col)[frame_number_col].agg(['min', 'max'])
    return output_frame_processing(category_ranges, cap)

def output_frame_processing(category_ranges, cap):
    output_videos = {}
    # Iterate through each category range and extract frames
    for category, frame_range in category_ranges.iterrows():
        category_start = int(frame_range['min'])
        category_end = int(frame_range['max'])

        # List to store frames for the current category
        frames = []

        # Set the video capture to the starting frame of the category
        cap.set(cv2.CAP_PROP_POS_FRAMES, category_start)

        # Iterate through frames in the category range
        for frame_number in range(category_start, category_end + 1):
            ret, frame = cap.read()
            if not ret:
                print('Cant read frame')
                break
            # Process the frame as needed (e.g., you can apply additional analysis or modifications here)

            # Append the frame to the list
            frames.append(frame)
        # Add the frames list to the output dictionary
        output_videos[category] = frames

    # Release the original video capture
    return output_videos


def out_put(category_ranges,cap):

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    x=94
    # Iterate through each category range and extract frames
    for category, frame_range in category_ranges.iterrows():
        category_start = int(frame_range['min'])
        category_end = int(frame_range['max'])

        # Create a VideoWriter object to save the extracted frames in .mp4 format
        if category==1:
            output_filename = f'1/{category}_{x}.mp4'
        elif category ==2:
            output_filename = f'2/{category}_{x}.mp4'
        elif category ==3:
            output_filename = f'3/{category}_{x}.mp4'
        elif category ==4:
            output_filename = f'4/{category}_{x}.mp4'
        elif category ==5:
            output_filename = f'5/{category}_{x}.mp4'
        # output_filename = f'{category}_{x}.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Use 'MJPG' or 'XVID' for AVI format
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height),
                              isColor=True)  # Adjust dimensions if needed

        # Set the video capture to the starting frame of the category
        cap.set(cv2.CAP_PROP_POS_FRAMES, category_start)

        # Iterate through frames in the category range
        for frame_number in range(category_start, category_end + 1):
            ret, frame = cap.read()
            if not ret:
                break
            # Process the frame as needed (e.g., you can apply additional analysis or modifications here)

            # Write the frame to the output video file
            out.write(frame)
        x+=1
        # Release the VideoWriter for this category
        out.release()