import pandas as pd
import cv2

def pre_processing(df, cap):
    df = df[['frame_number', 'category']]
    # categories = df['category'].unique()
    category_col = 'category'
    frame_number_col = 'frame_number'

    # Find unique categories in the DataFrame
    unique_categories = df['category'].unique()

    # Initialize variables to track frame ranges
    current_category = None
    start_frame = None
    frame_ranges = []

    # Iterate through the DataFrame to find frame ranges
    for index, row in df.iterrows():
        if current_category is None:
            # Initialize values for the first row
            current_category = row['category']
            start_frame = row['frame_number']
        elif row['category'] != current_category:
            # If category changes, store the frame range
            frame_ranges.append((start_frame, df.loc[index - 1, 'frame_number'], current_category))
            current_category = row['category']
            start_frame = row['frame_number']

    # Store the last frame range
    frame_ranges.append((start_frame, df['frame_number'].iloc[-1], current_category))

    # Create a new DataFrame with frame_start, frame_end, and category
    new_data = {'frame_start': [], 'frame_end': [], 'category': []}

    for frame_start, frame_end, category in frame_ranges:
        new_data['frame_start'].append(frame_start)
        new_data['frame_end'].append(frame_end)
        new_data['category'].append(category)

    df_new = pd.DataFrame(new_data)

    # # Find the indices where the category is not in numerical order
    # index_after_5 = df[df[category_col] == 5].index.max()
    #
    # # Keep all rows that come after the index with category 5
    # df_before_and_at_5 = df.loc[:index_after_5].reset_index(drop=True)
    # category_ranges = df_before_and_at_5.groupby(category_col)[frame_number_col].agg(['min', 'max'])
    return output_frame_processing(df_new, cap)
def output_frame_processing(category_ranges, cap):
    output_videos = {}
    frames_df = pd.DataFrame(columns=['frame_number', 'category'])
    # Iterate through each category range and extract frames
    for index, row in category_ranges.iterrows():
        category_start = int(row['frame_start'])
        category_end = int(row['frame_end'])

        # List to store frames for the current category
        frames_list=[]
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
            frames_list.append({'frame_number': frame_number, 'category': row['category']})
            # frames.append(frame)
        frames_df = pd.concat([frames_df, pd.DataFrame(frames_list)], ignore_index=True)

        # Add the frames list to the output dictionary
        # output_videos[row['category']] = frames

    # Release the original video capture
    # print(frames_df)
    return frames_df


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