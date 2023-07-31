from typing import Optional, Tuple

import cv2
import numpy as np

from supervision import Detections
from supervision.detection.utils import generate_2d_mask
from supervision.draw.color import Color
from supervision.draw.utils import draw_polygon, draw_text
from supervision.geometry.core import Position, Point
from supervision.geometry.utils import get_polygon_center


class PolygonZone:
    def __init__(
        self,
        polygon: np.ndarray,
        frame_resolution_wh: Tuple[int, int],
        triggering_position: Position = Position.BOTTOM_CENTER,
    ):
        self.polygon = polygon
        self.tracker_state: Dict[str, bool] = {}
        self.frame_resolution_wh = frame_resolution_wh
        self.triggering_position = triggering_position
        self.mask = generate_2d_mask(polygon=polygon, resolution_wh=frame_resolution_wh)
        self.current_count = 0

    def trigger(self, detections: Detections) -> np.ndarray:
        for xyxy, confidence, class_id, tracker_id in detections:
            # handle detections with no tracker_id
            if tracker_id is None:
                continue

            x1, y1, x2, y2 = xyxy
            anchors = [
            Point(x=(x1+x2)/2, y=(y1+y2)/2),
        ]
        triggers = self.mask[anchors[:, 1], anchors[:, 0]]
        
        if len(set(triggers)) == 2:
            continue

        tracker_state = triggers[0]

     # handle new detection
        if tracker_id not in self.tracker_state:
            self.tracker_state[tracker_id] = tracker_state
            continue
            
    # handle detection within polygon
        if self.tracker_state.get(tracker_id) == tracker_state:
            continue

        self.tracker_state[tracker_id] = tracker_state
        if tracker_state:
            self.current_count +=1
        # anchors = (
        #     np.ceil(
        #         detections.get_anchor_coordinates(anchor=self.triggering_position)
        #     ).astype(int)
        #     - 1
        # )

        
        
        #self.current_count = int(np.sum(is_in_zone))
        return is_in_zone.astype(bool)


class PolygonZoneAnnotator:
    def __init__(
        self,
        zone: PolygonZone,
        color: Color,
        thickness: int = 2,
        text_color: Color = Color.black(),
        text_scale: float = 0.5,
        text_thickness: int = 1,
        text_padding: int = 10,
    ):
        self.zone = zone
        self.color = color
        self.thickness = thickness
        self.text_color = text_color
        self.text_scale = text_scale
        self.text_thickness = text_thickness
        self.text_padding = text_padding
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.center = get_polygon_center(polygon=zone.polygon)

    def annotate(self, scene: np.ndarray, label: Optional[str] = None) -> np.ndarray:
        annotated_frame = draw_polygon(
            scene=scene,
            polygon=self.zone.polygon,
            color=self.color,
            thickness=self.thickness,
        )

        annotated_frame = draw_text(
            scene=annotated_frame,
            text= (f"litter: {str(self.zone.current_count)}") if label is None else label,
            text_anchor=self.center,
            background_color=self.color,
            text_color=self.text_color,
            text_scale=self.text_scale,
            text_thickness=self.text_thickness,
            text_padding=self.text_padding,
            text_font=self.font,
        )

        return annotated_frame
