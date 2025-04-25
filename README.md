# かんたん　あいづち　あかねちゃんシステム
茜ちゃんがword2vecを使って，適切な形容詞を返答するシステムです．
適切ではない場合も多いです．

# 内容
本リポジトリは、日本語自然言語処理および類似語検索を支援するツールです。  
※ モデルファイル（Word2Vec等）は含まれておりません。別途ご用意ください。
例：https://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/

## 🔧 必要な環境 / インストール

以下のPythonライブラリとmecabとが必要です：

```bash
pip install python3-mecab gensim tkinter
apt install mecab libmecab-dev mecab-ipadic
