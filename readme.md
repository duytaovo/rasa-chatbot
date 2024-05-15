# How to start Rasa chat bot

### Restore python virtual environment

```bash
python -m venv env                        # create virtual environment
# venv\Scripts\activate      
source .env/bin/activate               # activate environment
pip install -r requirements.txt           # install package
```


###  Rasa command

```bash
rasa train            # Trains a Rasa model using your NLU data and stories.
rasa interactive      # Starts an interactive learning session to create new  training data for a Rasa model by chatting.
rasa run              # Starts a Rasa server with your trained model.
rasa shell            # Loads your trained model and lets you talk to your assistant on the command line
```

### Note
On Debian you need the build-essential package:
```bash
sudo apt install build-essential
sudo apt install libpq-dev
```


I)installing rasa
>conda deactivate
>conda create -n rasaenv
>conda activate rasaenv
>pip install rasa
>rasa init
(install in current directory)


II)to communicate with rasa in cmd
>rasa shell

II)running rasa end points:
(rasaenv) E:\Automation\Bots\PersonalBot\Rasa>rasa run --cors "*" --enable-api

(rasaenv) E:\Automation\Bots\PersonalBot\Rasa>rasa run actions
rasa run -m models --enable-api --cors "*" --debug
uvicorn main:app --host 0.0.0.0 --port 5001
<!-- actions.py: Nơi bạn sẽ code tất cả mọi hành động tùy chỉnh mà bạn muốn bot làm
config.yml: Nơi bạn cấu hình các thông tin liên quan tới mô hình NLU và Core, cách mà chúng hoạt động.
credentials.yml: Thông tin chi tiết về cách kết nối chatbot với các dịch vụ như Facebook, Slack, Telegram,...
data/nlu.md: Dữ liệu huấn luyện cho NLU, bao gồm các câu được gán nhãn intent và entities theo định dạng cho trước.
data/stories.md: Dữ liệu huấn luyện cho Rasa core, là các kịch bản mà bạn muốn bot làm theo.
domain.yml: Đây coi như phần khai báo tất cả mọi thứ mà chatbot của bạn sử dụng, bao gồm các intent, entities, actions,...
endpoints.yml: Các endpoints mà bạn muốn chatbot trả ra
models/: Nơi lưu trữ các model bạn đã huấn luyện -->