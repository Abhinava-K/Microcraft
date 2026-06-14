# GitHub Repository Upload Guide

Follow these steps carefully to securely upload your **Microcraft** project to your GitHub repository.

> [!CAUTION]
> **Security Check:** Always ensure your `.env` file is excluded from git commits! If you upload your `.env` file containing your Groq and CoinGecko API keys, your keys will be compromised.
> *Note: We have already added `.env` to the `.gitignore` file for you, so your keys are safe to commit!*

---

### Step 1: Create a Repository on GitHub
1. Go to [GitHub](https://github.com/) and log in.
2. Click the **`+`** icon in the top right corner and select **New repository**.
3. Name your repository (e.g., `microcraft-ai-advisor`).
4. Leave it as **Public** or **Private** (Private is safer during active development).
5. **DO NOT** check the box to initialize with a README, `.gitignore`, or license (since you already have these files locally).
6. Click **Create repository**.

### Step 2: Initialize Git Locally
Open your VS Code terminal (make sure you are in the root `Microcraft` directory, not just inside `backend`) and run:
```bash
git init
```
*(If you have already initialized Git, you can skip this step).*

### Step 3: Stage and Commit Your Files
Stage all your files to be committed. Because we secured the `.gitignore`, the `.env` file and the virtual environment (`.venv`) will be safely ignored.
```bash
git add .
```
Now, create your first commit:
```bash
git commit -m "Initial commit: Set up AI Investment Advisor backend and documentation"
```

### Step 4: Link to GitHub and Set Branch
Rename your default branch to `main` (if it isn't already):
```bash
git branch -M main
```

Now, link your local repository to the GitHub repository you just created. Replace `<YOUR_USERNAME>` and `<YOUR_REPO_NAME>` with your actual GitHub username and repo name:
```bash
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
```

### Step 5: Push to GitHub
Finally, upload your code to the repository:
```bash
git push -u origin main
```

---

### Step 6: Verify Upload
1. Go back to your browser and refresh your GitHub repository page.
2. You should now see all your folders (`backend`, `markdowns`) and files (`notes.txt`).
3. **Crucial Verification:** Look inside the `backend` folder on GitHub. Ensure that you **DO NOT** see the `.env` file or the `.venv` folder. If they are absent, your upload was 100% secure and successful!
