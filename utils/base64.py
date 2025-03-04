import base64
import os

class AudioBase64Util:
    @staticmethod
    def audio_to_base64(file_path):
        """
        将本地音频文件读取为 Base64 编码格式。
        :param file_path: 音频文件的完整路径（包括文件名和后缀）
        :return: 文件的 Base64 编码字符串，或 None（如果发生异常）
        """
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            return None

        try:
            with open(file_path, "rb") as audio_file:
                # 读取音频文件的二进制数据
                audio_binary = audio_file.read()
                # 转换为 Base64 编码
                audio_base64 = base64.b64encode(audio_binary).decode("utf-8")
                return audio_base64
        except Exception as e:
            print(f"Error occurred while encoding file '{file_path}' to Base64: {e}")
            return None

    @staticmethod
    def save_base64_to_file(base64_data, output_file_path):
        """
        将 Base64 编码字符串保存为本地文件（恢复为原始二进制）。
        :param base64_data: Base64 编码字符串
        :param output_file_path: 输出文件路径
        :return: 是否保存成功（True/False）
        """
        try:
            # 将 Base64 解码为二进制数据
            audio_binary = base64.b64decode(base64_data)
            with open(output_file_path, "wb") as output_file:
                output_file.write(audio_binary)
            return True
        except Exception as e:
            print(f"Error occurred while saving Base64 data to file '{output_file_path}': {e}")
            return False
