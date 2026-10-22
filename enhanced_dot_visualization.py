# Enhanced Dotted Visualization for Harmony Project
# Based on Lucas-Kanade optical flow style dots

import cv2
import numpy as np
import math

def draw_optical_flow_dots(visual_feedback, prev_points, good_new, x1, y1, x2, y2, DOT_COLOR=(0, 0, 255)):
    """
    Create optical flow-style dotted visualization similar to Lucas-Kanade arrows
    """
    if prev_points is None or len(good_new) == 0:
        return
    
    # Calculate motion vectors for all points
    motion_vectors = []
    for i in range(min(len(prev_points), len(good_new))):
        prev_pt = prev_points[i].ravel()
        curr_pt = good_new[i].ravel()
        dx = curr_pt[0] - prev_pt[0]
        dy = curr_pt[1] - prev_pt[1]
        magnitude = math.sqrt(dx * dx + dy * dy)
        
        # Only consider points with significant movement
        if magnitude > 2.0:
            motion_vectors.append({
                'start': (int(prev_pt[0]), int(prev_pt[1])),
                'end': (int(curr_pt[0]), int(curr_pt[1])),
                'dx': dx,
                'dy': dy,
                'magnitude': magnitude
            })
    
    if not motion_vectors:
        return
    
    # Create optical flow dot pattern
    DOT_SPACING = 15  # Distance between dots in the flow pattern
    DOT_RADIUS = 2
    ARROW_LENGTH_SCALE = 3.0
    
    for vector in motion_vectors:
        start_x, start_y = vector['start']
        end_x, end_y = vector['end']
        dx, dy = vector['dx'], vector['dy']
        magnitude = vector['magnitude']
        
        # Scale the arrow length
        scaled_dx = dx * ARROW_LENGTH_SCALE
        scaled_dy = dy * ARROW_LENGTH_SCALE
        
        # Calculate number of dots to place along the flow line
        arrow_length = math.sqrt(scaled_dx**2 + scaled_dy**2)
        num_dots = max(3, int(arrow_length / DOT_SPACING))
        
        # Generate dots along the flow line
        for i in range(num_dots):
            t = i / (num_dots - 1)  # Parameter from 0 to 1
            
            # Interpolate position along the flow line
            dot_x = int(end_x + t * scaled_dx)
            dot_y = int(end_y + t * scaled_dy)
            
            # Make dots larger at the head (end) of the flow
            if i == num_dots - 1:  # Head dot
                dot_radius = DOT_RADIUS + 2
                dot_color = DOT_COLOR
            else:  # Flow trail dots
                dot_radius = DOT_RADIUS
                # Fade the trail dots based on position
                fade_factor = 0.3 + 0.7 * (i / (num_dots - 1))
                dot_color = (
                    int(DOT_COLOR[0] * fade_factor),
                    int(DOT_COLOR[1] * fade_factor),
                    int(DOT_COLOR[2] * fade_factor)
                )
            
            # Draw the dot
            cv2.circle(visual_feedback, (dot_x, dot_y), dot_radius, dot_color, -1)
        
        # Add perpendicular dots to show flow direction (like arrow head)
        if magnitude > 5.0:  # Only for significant motion
            angle = math.atan2(scaled_dy, scaled_dx)
            perp_angle = angle + math.pi / 2
            
            # Create small perpendicular dots at the head
            head_x = end_x + scaled_dx
            head_y = end_y + scaled_dy
            
            for offset in [-8, 8]:
                perp_x = int(head_x + offset * math.cos(perp_angle))
                perp_y = int(head_y + offset * math.sin(perp_angle))
                cv2.circle(visual_feedback, (perp_x, perp_y), DOT_RADIUS, DOT_COLOR, -1)

def enhance_waste_box_dots(visual_feedback, waste_box, motion_vectors=None):
    """
    Enhanced waste box visualization with motion-responsive dots
    """
    if waste_box is None:
        return
    
    x1, y1, x2, y2 = map(int, waste_box)
    
    # Base dot configuration
    DOT_COLOR = (0, 0, 255)
    OUTLINE_RADIUS = 4
    INTERIOR_RADIUS = 2
    OUTLINE_COUNT = 12
    INTERIOR_STEP = 25
    
    # --- Enhanced outline with motion-responsive dots ---
    for i in range(OUTLINE_COUNT):
        t = i / (OUTLINE_COUNT - 1)
        top_x = int(x1 + (x2 - x1) * t)
        bot_x = int(x1 + (x2 - x1) * t)
        left_y = int(y1 + (y2 - y1) * t)
        right_y = int(y1 + (y2 - y1) * t)
        
        # Make outline dots pulse when there's motion
        radius = OUTLINE_RADIUS
        if motion_vectors and len(motion_vectors) > 0:
            radius = OUTLINE_RADIUS + 1  # Slightly larger when moving
        
        cv2.circle(visual_feedback, (top_x, y1), radius, DOT_COLOR, -1)     # top
        cv2.circle(visual_feedback, (bot_x, y2), radius, DOT_COLOR, -1)     # bottom
        cv2.circle(visual_feedback, (x1, left_y), radius, DOT_COLOR, -1)     # left
        cv2.circle(visual_feedback, (x2, right_y), radius, DOT_COLOR, -1)   # right
    
    # --- Enhanced interior with flow-aware dots ---
    inset = 10
    for iy in range(y1 + inset, y2 - inset, INTERIOR_STEP):
        for ix in range(x1 + inset, x2 - inset, INTERIOR_STEP):
            # Vary dot size based on motion proximity
            radius = INTERIOR_RADIUS
            if motion_vectors:
                # Check if this dot is near any motion vector
                for vector in motion_vectors:
                    dist = math.sqrt((ix - vector['end'][0])**2 + (iy - vector['end'][1])**2)
                    if dist < 30:  # Near motion
                        radius = INTERIOR_RADIUS + 1
                        break
            
            cv2.circle(visual_feedback, (ix, iy), radius, DOT_COLOR, -1)
