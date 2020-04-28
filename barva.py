# pred_maske = outputs["instances"].get("pred_masks")
# Array za vsak instance posebej. Torej če zazna dvanajst objekotv ima array 12 elementov

def barve(pred_maske):
  pred_maske_cpu = np.array(pred_maske[0].cpu())
  maska = np.where(pred_maske_cpu == True)
  x, y = maska
  colors = [255, 223, 191, 159, 127, 95, 63, 31, 0]

  original_color_count = {}
  color_count = {}
  # Loop through every pixel in the image and modify it
  for i in range(len(x)):
    current_color = tuple(im[x[i]][y[i]])  
    if current_color in original_color_count:
      original_color_count[current_color] += 1
    else:
      original_color_count[current_color] = 1


    r, g, b = current_color
    r_set = False
    g_set = False
    b_set = False

          #  Loop through our allowed values and find the closest value to snap to
    for i in range(len(colors)):
        color_one = colors[i]
        color_two = colors[i + 1]

        if not r_set:
            if color_one >= r >= color_two:
                distance_one = color_one - r
                distance_two = r - color_two
                r = color_one if distance_one <= distance_two else color_two
                r_set = True

        if not g_set:
            if color_one >= g >= color_two:
                distance_one = color_one - g
                distance_two = g - color_two
                g = color_one if distance_one <= distance_two else color_two
                g_set = True

        if not b_set:
            if color_one >= b >= color_two:
                distance_one = color_one - b
                distance_two = b - color_two
                b = color_one if distance_one <= distance_two else color_two
                b_set = True

        if all((r_set, g_set, b_set)):
            break

    # Set our new pixel back on the image to see the difference
    new_rgb = [r, g, b]
  
    im[x[i]][y[i]] = new_rgb
    new_rgb = tuple(new_rgb)
    if new_rgb in color_count:
        color_count[new_rgb] += 1
    else:
        color_count[new_rgb] = 1

  # Save our new image


  # Count and sort the colors
  all_colors = color_count.items()
  all_colors = sorted(all_colors, key=lambda tup: tup[1], reverse=True)

  # Print out the colors
  print("## All Colors ##")
  for i in range(10):
    print(all_colors[i])

  # Remove black, white and gray
  print("\n## All Colors Filtered ##")
  filtered_colors = [color for color in all_colors if not color[0][0] == color[0][1] == color[0][2]]
  for i in range(10):
    print(filtered_colors[i])

  print("")
  original_color_count = len(original_color_count)
  print("Original Color Count: {}".format(original_color_count))
  new_color_count = len(color_count)
  print("New Color Count: {}".format(new_color_count))
  color_diff = original_color_count - new_color_count
  print("Reduced Color Count By: {}".format(color_diff))
