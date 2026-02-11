# Order wise commands
```
npm start
git add data.json view.html
git commit -m "Update list"
git push

if port not closed use
fuser -k 3000/tcp

fuser -k 3000/tcp
```

---
Ctrl + C

## Step 3: Stop the Codespace (Important!)

Don't just close the browser tab — that leaves the Codespace running in the background (and eats your free hours).

**Proper way to stop:**
1. Click the **green button** at the bottom-left of VS Code (shows the Codespace name)
2. Click **"Stop Current Codespace"**

**OR** go to [github.com/codespaces](https://github.com/codespaces):
1. Find your Codespace
2. Click the **"..."** menu next to it
3. Click **"Stop codespace"**

---

## Step 4: Next Time You Come Back
1. Go to [github.com/codespaces](https://github.com/codespaces)
2. Click your existing Codespace (don't create a new one!)
3. Terminal will open fresh — just run `npm start` again

---

## Summary
```
Ctrl+C          → stops server
fuser -k 3000/tcp  → frees the port
Stop Codespace  → saves your free hours
```
