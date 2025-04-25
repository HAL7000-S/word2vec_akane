import MeCab
from gensim.models import KeyedVectors
import time

# データベース
# https://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/

import tkinter as tk
from PIL import Image, ImageTk
import time

# 画像の読み込み
base_image = Image.open("base.png")
speek_image = Image.open("speek.png")

class TalkSystem:
    def __init__(self, model_path='./entity_vector.model.bin'):
    
        self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)

        self.tagger = MeCab.Tagger()
        self.tagger.parse("")  # バグ対策のため初回空解析

    def extract_adjectives(self, text):
        """MeCabで形容詞を抽出"""
        node = self.tagger.parseToNode(text)

        adjectives = []
        while node:
            features = node.feature.split(",")
            if features[0] in "形容詞":
                base_form = features[6]  # 基本形
                if base_form != "*":
                    adjectives.append(base_form)
            node = node.next
        return adjectives

    def extract_all_words(self, text):
        """形態素解析で全単語（名詞・動詞・形容詞・副詞など）を抽出"""
        node = self.tagger.parseToNode(text)

        words = []
        while node:
            surface = node.surface
            features = node.feature.split(",")
            if features[0] in ["名詞", "動詞", "形容詞", "副詞"]:
                words.append(surface)
            node = node.next
        return words

    def get_near_adjectives(self, input_text, topn=30):
        total_start = time.time()
        start = time.time()

        """入力文から近い形容詞を返す"""
        all_words = self.extract_all_words(input_text)
        print("単語:",all_words)
        adjectives_in_model = [w for w in all_words if w in self.model]

        print("単語ベクトル抽出完了:", time.time() - start, "秒")
        start = time.time()

        if not adjectives_in_model:
            print("モデルに含まれる単語が見つかりませんでした。")
            return input_text

        vector_sum = sum([self.model[w] for w in adjectives_in_model])

        # cosine similarityの計算
        results = self.model.similar_by_vector(vector_sum, topn=topn)
        print(results)
        print("全体処理時間:", time.time() - total_start, "秒")

        for result in results:
            adjective = self.extract_adjectives(result[0])
            if adjective != []:
                return adjective[0]
        return input_text

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("かんたん あいづち あかねちゃん")

        # 外に準備した関数立ち上げ
        model_path = './entity_vector.model.bin'  # KeyedVectors形式
        self.talk_system = TalkSystem(model_path)

        # フレーム構成
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", padx=20, pady=20)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right")

        # 入力欄
        self.input_box = tk.Entry(self.left_frame, font=("Arial", 14), width=30)
        self.input_box.pack(pady=5)

        # 実行ボタン
        self.button = tk.Button(self.left_frame, text="送信", command=self.on_run, font=("Arial", 12))
        self.button.pack(pady=5)

        # 出力欄
        self.output_label = tk.Label(self.left_frame, text="", font=("Arial", 14), bg="white", wraplength=350, justify="left")
        self.output_label.pack(pady=5)
        self.output_label.config(text=f"茜ちゃん「・・・」")

        # 画像キャンバス
        self.bg_image = ImageTk.PhotoImage(base_image)
        self.speek_image = ImageTk.PhotoImage(speek_image)
        self.canvas = tk.Canvas(self.right_frame, width=self.bg_image.width(), height=self.bg_image.height(), highlightthickness=0)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.pack()

    def on_run(self):
        user_input = self.input_box.get()

        # speek.png を表示
        self.canvas.itemconfig(self.bg_id, image=self.speek_image)
        self.root.update()

        # word2vec処理
        similar_adj = self.talk_system.get_near_adjectives(user_input)

        output_word = similar_adj+"やで"
        if user_input[-1] == "イ" or user_input[-1] == "い":
            output_word = user_input[:-1]+"い やで"

        # 出力
        self.output_label.config(text=f"茜ちゃん「{output_word}」")
        self.root.update()
        time.sleep(2)

        self.canvas.itemconfig(self.bg_id, image=self.bg_image)
        # self.root.after(500, lambda: self.canvas.itemconfig(self.bg_id, image=self.bg_image))






# 実行
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()