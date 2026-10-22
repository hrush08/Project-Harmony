# Optical Flow Dotted Visualization for Harmony Project
# Similar to Lucas-Kanade optical flow arrows but using dots

import cv2
import numpy as np
import math

def draw_optical_flow_dots(visual_feedback, prev_points, good_new, DOT_COLOR=(0, 0, 255)):
    """
    Draw optical flow visualization using dots instead of arrows
    Similar to the Lucas-Kanade optical flow example
    """
    if prev_points is None or len(good_new) == 0:
        return
    
    # Calculate motion vectors
    motion_vectors = []
    for i in range(min(len(prev_points), len(good_new))):
        prev_pt = prev_points[i].ravel()
        curr_pt = good_new[i].ravel()
        dx = curr_pt[0] - prev_pt[0]
        dy = curr_pt[1] - prev_pt[1]
        magnitude = math.sqrt(dx * dx + dy * dy)
        
        if magnitude > 2.0:  # Only significant movements
            motion_vectors.append({
                'start': (int(prev_pt[0]), int(prev_pt[1])),
                'end': (int(curr_pt[0]), int(curr_pt[1])),
                'dx': dx,
                'dy': dy,
                'magnitude': magnitude
            })
    
    if not motion_vectors:
        return
    
    # Draw optical flow dots
    DOT_SPACING = 12
    DOT_RADIUS = 2
    ARROW_LENGTH_SCALE = 3.0
    
    for vector in motion_vectors:
        start_x, start_y = vector['start']
        end_x, end_y = vector['end']
        dx, dy = vector['dx'], vector['dy']
        
        # Scale the flow vector
        scaled_dx = dx * ARROW_LENGTH_SCALE
        scaled_dy = dy * ARROW_LENGTH_SCALE
        
        # Calculate number of dots along the flow line
        arrow_length = math.sqrt(scaled_dx**2 + scaled_dy**2)
        num_dots = max(3, min(8, int(arrow_length / DOT_SPACING)))
        
        # Draw dots along the flow direction
        for i in range(num_dots):
            t = i / max(1, (num_dots - 1))  # Avoid division by zero
            
            # Position along the flow line
            dot_x = int(end_x + t * scaled_dx)
            dot_y = int(end_y + t * scaled_dy)
            
            # Larger, brighter dot at the head (like arrow tip)
            if i == num_dots - 1:
                dot_radius = DOT_RADIUS + 2
                dot_color = DOT_COLOR
            else:
                # Fading trail dots
                dot_radius = DOT_RADIUS
                fade_factor = 0.3 + 0.7 * (i / max(1, (num_dots - 1)))
                dot_color = (
                    int(DOT_COLOR[0] * fade_factor),
                    int(DOT_COLOR[1] * fade_factor),
                    int(DOT_COLOR[2] * fade_factor)
                )
            
            cv2.circle(visual_feedback, (dot_x, dot_y), dot_radius, dot_color, -1)
        
        # Add perpendicular dots to show direction (like arrow head)
        if vector['magnitude'] > 5.0:
            angle = math.atan2(scaled_dy, scaled_dx)
            perp_angle = angle + math.pi / 2
            
            head_x = end_x + scaled_dx
            head_y = end_y + scaled_dy
            
            # Small dots perpendicular to flow direction
            for offset in [-6, 6]:
                perp_x = int(head_x + offset * math.cos(perp_angle))
                perp_y = int(head_y + offset * math.sin(perp_angle))
                cv2.circle(visual_feedback, (perp_x, perp_y), DOT_RADIUS, DOT_COLOR, -1)

def enhance_waste_box_dots(visual_feedback, waste_box, motion_active=False):
    """
    Enhanced waste box visualization with motion-responsive dots
    """
    if waste_box is None:
        return
    
    x1, y1, x2, y2 = map(int, waste_box)
    
    # Dot configuration
    DOT_COLOR = (0, 0, 255)
    OUTLINE_RADIUS = 4
    INTERIOR_RADIUS = 2
    OUTLINE_COUNT = 12
    INTERIOR_STEP = 25
    
    # Enhanced outline - pulse when there's motion
    current_radius = OUTLINE_RADIUS + (1 if motion_active else 0)
    
    # Draw outline dots
    for i in range(OUTLINE_COUNT):
        t = i / max(1, (OUTLINE_COUNT - 1))
        top_x = int(x1 + (x2 - x1) * t)
        bot_x = int(x1 + (x2 - x1) * t)
        left_y = int(y1 + (y2 - y1) * t)
        right_y = int(y1 + (y2 - y1) * t)
        
        cv2.circle(visual_feedback, (top_x, y1), current_radius, DOT_COLOR, -1)     # top
        cv2.circle(visual_feedback, (bot_x, y2), current_radius, DOT_COLOR, -1)     # bottom
        cv2.circle(visual_feedback, (x1, left_y), current_radius, DOT_COLOR, -1)     # left
        cv2.circle(visual_feedback, (x2, right_y), current_radius, DOT_COLOR, -1)   # right
    
    # Enhanced interior dots
    inset = 10
    for iy in range(y1 + inset, y2 - inset, INTERIOR_STEP):
        for ix in range(x1 + inset, x2 - inset, INTERIOR_STEP):
            # Make interior dots slightly larger when there's motion
            current_interior_radius = INTERIOR_RADIUS + (1 if motion_active else 0)
            cv2.circle(visual_feedback, (ix, iy), current_interior_radius, DOT_COLOR, -1)
