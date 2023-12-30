import numpy as np

class PoseClassifier:
    def __init__(self, data):
        self.data = data
        self.body_length = self.calculate_body_length()
    
    def calculate_body_length(self):
        head_chest_length = np.sqrt((self.data['head_x'] - self.data['chest_x'])**2 + (self.data['head_y'] - self.data['chest_y'])**2)
        chest_hip_length = np.sqrt((self.data['chest_x'] - self.data['hip_x'])**2 + (self.data['chest_y'] - self.data['hip_y'])**2)
        hip_right_knee_length = np.sqrt((self.data['hip_x'] - self.data['knee_right_x'])**2 + (self.data['hip_y'] - self.data['knee_right_y'])**2)
        right_knee_foot_length = np.sqrt((self.data['knee_right_x'] - self.data['foot_right_x'])**2 + (self.data['knee_right_y'] - self.data['foot_right_y'])**2)
        hip_left_knee_length = np.sqrt((self.data['hip_x'] - self.data['knee_left_x'])**2 + (self.data['hip_y'] - self.data['foot_left_y'])**2)
        left_knee_foot_length = np.sqrt((self.data['knee_left_x'] - self.data['foot_left_x'])**2 + (self.data['knee_left_y'] - self.data['foot_left_y'])**2)
        right_length = head_chest_length + chest_hip_length + hip_right_knee_length + right_knee_foot_length
        left_length = head_chest_length + chest_hip_length + hip_left_knee_length + left_knee_foot_length
        if right_length > left_length:
            body_length = right_length
        else:
            body_length = left_length
        return body_length
            
    def is_horizontal(self, y_values):
        tolerance = 0.1 * self.body_length  # Dynamic tolerance
        return np.std(y_values) < tolerance

    def angle_between_points(self, x1, y1, x2, y2):
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        return angle

    def is_diagonal(self, x1, y1, x2, y2):
        angle = self.angle_between_points(x1, y1, x2, y2)
        return 30 <= abs(angle) <= 55  # Adjusted to a range around 45 degrees

    def classify_pose(self):
        
        # Extract coordinates
        head_x, head_y = self.data['head_x'], self.data['head_y']
        chest_x, chest_y = self.data['chest_x'], self.data['chest_y']
        hip_x, hip_y = self.data['hip_x'], self.data['hip_y']
        knee_right_x, knee_right_y = self.data['knee_right_x'], self.data['knee_right_y']
        knee_left_x, knee_left_y = self.data['knee_left_x'], self.data['knee_left_y']
        foot_right_x, foot_right_y = self.data['foot_right_x'], self.data['foot_right_y']
        foot_left_x, foot_left_y = self.data['foot_left_x'], self.data['foot_left_y']

        # Check for inversion first
        angleR = self.angle_between_points(head_x, head_y, foot_right_x, foot_right_y)
        angleL = self.angle_between_points(head_x, head_y, foot_left_x, foot_left_y)
        
        if head_y > chest_y > hip_y or (angleR < 0 and angleL < 0):
            return 'inverted'

        # Calculate slopes for potential diagonal lines
        right_side_slope = self.is_diagonal(head_x, head_y, foot_right_x, foot_right_y)
        left_side_slope = self.is_diagonal(head_x, head_y, foot_left_x, foot_left_y)

        # Check for diagonal pose
        if right_side_slope or left_side_slope:
            return 'diagonal'

        # Check for horizontal pose
        if self.is_horizontal([head_y, chest_y, hip_y]):
            return 'horizontal'

        # Check for upright pose
        if head_y < chest_y < hip_y:
            return 'upright'

        return 'undefined'
        
# Function to classify the row orientation
def classify_row_orientation(row):
    classifier = PoseClassifier(row)
    return classifier.classify_pose()