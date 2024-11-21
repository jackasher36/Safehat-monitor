package org.jackasher.safehat.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
@RequestMapping("/api")
public class SafeHatController {

    private static final String PYTHON_SCRIPT_IMAGE = "/Users/leojackasher/PycharmProjects/PythonProject2/image_detect.py";
    private static final String PYTHON_SCRIPT_VIDEO = "/Users/leojackasher/PycharmProjects/PythonProject2/video_detect.py";
    private static final String FILE_SAVE_DIR = "/Users/leojackasher/IdeaProjects/SafeHat/src/main/resources/uploads/";

    // 支持的视频文件类型
    private static final String[] VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".gif"};

    @PostMapping("/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return "文件上传失败，请选择一个文件！";
        }

        try {
            // 保存上传的文件
            String fileName = file.getOriginalFilename();
            String filePath = FILE_SAVE_DIR + fileName;
            byte[] bytes = file.getBytes();
            Path path = Paths.get(filePath);
            Files.write(path, bytes);

            // 判断文件类型
            String fileType = Files.probeContentType(path);
            System.out.println("文件类型：" + fileType);

            String pythonScript = null;

            // 如果文件类型是图片，使用图片推理脚本
            if (fileType != null && fileType.startsWith("image")) {
                if (fileType.endsWith("gif")) {
                    pythonScript = PYTHON_SCRIPT_VIDEO;
                }else {
                       pythonScript = PYTHON_SCRIPT_IMAGE;
                }

            }
            // 如果文件类型是视频或者是gif，使用视频推理脚本
            else if (fileType != null && isVideoFile(fileName)) {
                pythonScript = PYTHON_SCRIPT_VIDEO;
            } else {
                return "不支持的文件类型！";
            }

            System.out.println("调用的Python脚本：" + pythonScript);

            // 调用 Python 脚本进行推理
            ProcessBuilder processBuilder = new ProcessBuilder("python3", pythonScript, filePath);
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            // 获取 Python 推理结果
            String result = new String(process.getInputStream().readAllBytes());
            process.waitFor();

            return result.split("spilt")[1];
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return "文件上传或处理失败：" + e.getMessage();
        }
    }

    /**
     * 检查文件是否为视频类型
     * @param fileName 文件名
     * @return true 如果文件是视频类型
     */
    private boolean isVideoFile(String fileName) {
        String lowerCaseFileName = fileName.toLowerCase();
        for (String ext : VIDEO_EXTENSIONS) {
            if (lowerCaseFileName.endsWith(ext)) {
                return true;
            }
        }
        return false;
    }
}