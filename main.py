import cv2 as cv
import numpy as np
import pyrealsense2 as rs


def find_yutou(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # find white bg as roi
    _, thresh = cv.threshold(gray, 110, 255, cv.THRESH_BINARY)
    # _, thresh = cv.adaptiveThreshold(
    #     gray, 100, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 10
    # )
    # find contours
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # find the biggest contour
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    # draw the contour
    # cv.drawContours(img, [max_contour], -1, (0, 255, 0), 2)
    # find the bounding box
    x, y, w, h = cv.boundingRect(max_contour)
    roi = img[y : y + h, x : x + w]
    # cv.imshow("roi", roi)
    # cv.waitKey(0)
    # find yutou with darker color
    roi_gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    _, roi_thresh = cv.threshold(roi_gray, 120, 180, cv.THRESH_BINARY_INV)
    # _, roi_thresh = cv.adaptiveThreshold(
    #     roi_gray, 150, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 10
    # )
    cv.imshow("roi_thresh", roi_thresh)
    # cv.waitKey(0)
    roi_contours, _ = cv.findContours(
        roi_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
    )
    # find the biggest contour
    max_area = 0
    max_contour = None
    for contour in roi_contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    # draw the contour
    # cv.drawContours(roi, [max_contour], -1, (0, 255, 0), 2)
    # find the bounding box
    rx, ry, rw, rh = cv.boundingRect(max_contour)
    # img = cv.rectangle(roi, (rx, ry), (rx + rw, ry + rh), (0, 255, 0), 2)
    yutou = roi[ry : ry + rh, rx : rx + rw]
    # cv.imshow("yutou", yutou)
    # cv.imshow("image", img)
    # cv.waitKey(0)
    real_countour = max_contour + np.array([x, y])
    pos2origin = {
        "x": x + rx,
        "y": y + ry,
        "w": rw,
        "h": rh,
        "cx": x + rx + rw / 2,
        "cy": y + ry + rh / 2,
        "edge": real_countour,
    }
    return yutou, pos2origin


pipeline, config, device, device_product_line = None, None, None, None
found_rgb, pipeline_wrapper, pipeline_profile = None, None, None


def init_depth():
    global pipeline, config, device, device_product_line
    global found_rgb, pipeline_wrapper, pipeline_profile

    pipeline = rs.pipeline()
    config = rs.config()

    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == "RGB Camera":
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    if device_product_line == "L500":
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)


def get_depth():
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    return depth_image, color_image


if __name__ == "__main__":
    # for i in range(0, 14):
    #     image = cv.imread(f"yutou/images/train/{i:04d}.jpg")
    #     img, pos = find_yutou(image)
    #     cv.rectangle(image, (pos['x'], pos['y']), (pos['x'] + pos['w'], pos['y'] + pos['h']), (0, 255, 0), 2)
    #     cv.drawContours(image, [pos['edge']], -1, (0, 255, 0), 2)
    #     cv.circle(image, (int(pos['cx']), int(pos['cy'])), 2, (0, 0, 255), 2)

    #     cv.imshow("yutou", img)
    #     cv.imshow("image", image)
    #     cv.waitKey(0)
    # init_depth()
    cap = cv.VideoCapture('sssss.mp4')
    mp4 = cv.VideoWriter_fourcc(*'mp4v')
    _, color = cap.read()
    color = color[300:1000, :]
    save = cv.VideoWriter('output.mp4', mp4, 30, color.shape[1::-1])
    while True:
        try:
        # depth, color = get_depth()
            _, color = cap.read()
            color = color[300:1000, :]
            depth = np.zeros_like(color)
            dist = 0
            img, pos = find_yutou(color)
            cv.rectangle(
                color,
                (pos["x"], pos["y"]),
                (pos["x"] + pos["w"], pos["y"] + pos["h"]),
                (0, 0, 255),
                2,
            )
            # cv.drawContours(color, [pos["edge"]], -1, (0, 0, 255), 2)
            cv.circle(color, (int(pos["cx"]), int(pos["cy"])), 2, (0, 0, 255), 2)
            dist = depth[int(pos["cy"]), int(pos["cx"])]
            # cv.putText(
            #     color,
            #     f"{dist}mm",
            #     (int(pos["cx"]), int(pos["cy"])),
            #     cv.FONT_HERSHEY_SIMPLEX,
            #     1,
            #     (0, 255, 0),
            #     2,
            #     cv.LINE_AA,
            # )
            cv.imshow("yutou", img)
            cv.imshow("image", color)
            save.write(color)
        except:
            # cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            save.release()
            break
        k = cv.waitKey(0)
        if k == ord("q"):
            break
