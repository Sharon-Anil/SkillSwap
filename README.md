# 🌟 SkillSwap – Learn, Teach, Earn

SkillSwap is a **YouTube-style skill-sharing platform** where users can become creators, upload videos, and earn through a unique coin-based reward system. Viewers can use **SuperCoins** to unlock premium videos and **freely access** select content, all while engaging in a secure, anonymous chat with creators.

---

## 🚀 Features

🔹 **Creator Dashboard**  
- Upload videos  
- Set videos as "Free" or "Paid"  
- Track SuperCoins earned  
- Manage your profile and channel  

🔹 **Viewer Dashboard**  
- Search and discover creators  
- Unlock paid videos using SuperCoins  
- Watch free videos instantly  
- View creator's channel, profile, and uploaded videos  
- Private SkillSwap chat system with creators (no phone/email)  

🔹 **Search System**  
- Search by channel name (e.g., *ArtZone*, *CodeMaster*)  
- Get channel overview, creator profile, and videos  

🔹 **Coin Unlock System**  
- Viewers spend coins to unlock content  
- Creators earn coins for each video unlocked  
- Free videos can be watched instantly  

🔹 **Secure Chat**  
- End-to-end encrypted private chat  
- Viewers and creators communicate using SkillSwap IDs  
- No personal data like phone numbers or emails revealed  

---

## 💼 Use Case

**For Students & Learners:**  
Quickly discover practical skills from creators and educators. Use coins wisely to unlock the most valuable content.

**For Creators & Teachers:**  
Share your knowledge, build your audience, and earn SuperCoins from your content. A better alternative to ad-based revenue.

**For Entrepreneurs & Coaches:**  
Create your own channel to monetize your skills directly without middlemen.

---

## 💰 Monetization Potential

SkillSwap introduces a **SuperCoin economy**:
- Creators earn from each unlock.
- Viewers can recharge or earn coins through engagement.
- Ideal for **freelancers, coaches, educators**, and **side hustlers**.

---

## 📦 Project Structure

skillswap/
├── app/
│ ├── templates/
│ │ ├── viewer_dashboard.html
│ │ ├── creator_dashboard.html
│ │ ├── view_channel.html
│ │ └── ...
│ ├── static/
│ ├── routes.py
│ ├── models.py
│ └── init.py
├── seed_dummy_data.py
├── run.py
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🛠️ Technologies Used

- **Python Flask** (Backend)
- **SQLite** (Database)
- **HTML, CSS, JavaScript** (Frontend)
- **Ngrok / Cloudflare Tunnel** for local hosting
- **Bootstrap / Tailwind** for responsive UI

---

## 🧪 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YourUsername/SkillSwap.git
cd SkillSwap

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Seed dummy data (once)
python seed_dummy_data.py

# 5. Run the app
python run.py
