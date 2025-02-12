import os
import requests
import concurrent.futures

def download_file(url, download_folder):
    filename = os.path.join(download_folder, os.path.basename(url))
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"已下载: {filename}")
        return filename
    else:
        print(f"下载失败: {url}")
        return None

def extract_kasumi_voice(input_file, output_file, target_name="香澄", download_folder="./voice"):
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
        
        kasumi_lines = [line for line in lines if "|" + target_name + "|" in line]
        
        os.makedirs(download_folder, exist_ok=True)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
            future_to_url = {executor.submit(download_file, line.split("|")[0], download_folder): line for line in kasumi_lines}
            
            results = []
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future].split("|")[0]
                filename = future.result()
                if filename:
                    parts = future_to_url[future].strip().split("|", 2)
                    results.append(f"{filename}|{parts[1]}|{parts[2]}\n")
        
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.writelines(results)
        
        print(f"提取完成，共 {len(results)} 条记录，已保存到 {output_file}")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    extract_kasumi_voice("SortPathUrl.txt", "KasumiVoiceUrls.txt")
