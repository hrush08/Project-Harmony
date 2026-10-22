# Enhanced Arrow Visualization for Harmony Project
# Short triangular red arrows like in the provided image

import cv2
import numpy as np
import math

def draw_short_triangular_arrows(visual_feedback, prev_points, good_new, waste_box=None, ARROW_COLOR=(0, 0, 255)):
    """
    Draw short triangular red arrows similar to the image style
    Arrows originate from moving objects and point in direction of motion
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
        
        # Only consider significant movements
        if magnitude > 1.5:  # Lower threshold for more sensitive detection
            motion_vectors.append({
                'start': (int(prev_pt[0]), int(prev_pt[1])),
                'end': (int(curr_pt[0]), int(curr_pt[1])),
                'dx': dx,
                'dy': dy,
                'magnitude': magnitude
            })
    
    if not motion_vectors:
        return
    
    # Draw short triangular arrows
    ARROW_LENGTH = 15  # Short arrows like in the image
    ARROW_WIDTH = 8     # Width of the arrow base
    MIN_SPACING = 25    # Minimum spacing between arrows to avoid clutter
    
    # Filter arrows to avoid too much clutter
    filtered_arrows = []
    for vector in motion_vectors:
        # Check if this arrow is too close to existing ones
        too_close = False
        for existing in filtered_arrows:
            dist = math.sqrt((vector['start'][0] - existing['start'][0])**2 + 
                           (vector['start'][1] - existing['start'][1])**2)
            if dist < MIN_SPACING:
                too_close = True
                break
        
        if not too_close:
            filtered_arrows.append(vector)
    
    # Draw the filtered arrows
    for vector in filtered_arrows:
        start_x, start_y = vector['start']
        dx, dy = vector['dx'], vector['dy']
        magnitude = vector['magnitude']
        
        # Calculate arrow direction and length
        if magnitude > 0:
            # Normalize and scale the arrow
            arrow_dx = (dx / magnitude) * ARROW_LENGTH
            arrow_dy = (dy / magnitude) * ARROW_LENGTH
            
            # Arrow tip position
            tip_x = int(start_x + arrow_dx)
            tip_y = int(start_y + arrow_dy)
            
            # Calculate perpendicular for triangle base
            perp_dx = -arrow_dy / ARROW_LENGTH * ARROW_WIDTH / 2
            perp_dy = arrow_dx / ARROW_LENGTH * ARROW_WIDTH / 2
            
            # Triangle base points
            base1_x = int(start_x + perp_dx)
            base1_y = int(start_y + perp_dy)
            base2_x = int(start_x - perp_dx)
            base2_y = int(start_y - perp_dy)
            
            # Draw filled triangle arrow
            triangle_points = np.array([
                [tip_x, tip_y],
                [base1_x, base1_y],
                [base2_x, base2_y]
            ], np.int32)
            
            cv2.fillPoly(visual_feedback, [triangle_points], ARROW_COLOR)
            
            # Add a small circle at the base for better visibility
            cv2.circle(visual_feedback, (start_x, start_y), 2, ARROW_COLOR, -1)

def enhance_waste_detection_arrows(visual_feedback, waste_box, motion_active=False):
    """
    Enhanced waste box visualization with arrow indicators
    """
    if waste_box is None:
        return
    
    x1, y1, x2, y2 = map(int, waste_box)
    
    # Arrow configuration
    ARROW_COLOR = (0, 0, 255)
    OUTLINE_RADIUS = 4
    INTERIOR_RADIUS = 2
    OUTLINE_COUNT = 12
    INTERIOR_STEP = 25
    
    # Enhanced outline with motion-responsive arrows
    for i in range(OUTLINE_COUNT):
        t = i / max(1, (OUTLINE_COUNT - 1))
        top_x = int(x1 + (x2 - x1) * t)
        bot_x = int(x1 + (x2 - x1) * t)
        left_y = int(y1 + (y2 - y1) * t)
        right_y = int(y1 + (y2 - y1) * t)
        
        # Make outline dots pulse when there's motion
        radius = OUTLINE_RADIUS
        if motion_active:
            radius = OUTLINE_RADIUS + 1
        
        cv2.circle(visual_feedback, (top_x, y1), radius, ARROW_COLOR, -1)     # top
        cv2.circle(visual_feedback, (bot_x, y2), radius, ARROW_COLOR, -1)     # bottom
        cv2.circle(visual_feedback, (x1, left_y), radius, ARROW_COLOR, -1)     # left
        cv2.circle(visual_feedback, (x2, right_y), radius, ARROW_COLOR, -1)   # right
    
    # Enhanced interior with flow-aware dots
    inset = 10
    for iy in range(y1 + inset, y2 - inset, INTERIOR_STEP):
        for ix in range(x1 + inset, x2 - inset, INTERIOR_STEP):
            radius = INTERIOR_RADIUS
            if motion_active:
                radius = INTERIOR_RADIUS + 1
            
            cv2.circle(visual_feedback, (ix, iy), radius, ARROW_COLOR, -1)
