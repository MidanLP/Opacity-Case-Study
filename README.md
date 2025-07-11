# Opacity Case Study

This project supports the case study and practical evaluation for the thesis **"Analyzing System Confidentiality: A Case Study of a Real-World System using Timed Automata"** submitted at TU Berlin. It includes simulation scripts, verification data, and a web system used to illustrate and benchmark opacity in discrete-timed systems.

---

## Project Structure

- `Testing/` – Contains files and scipts for testing of the Website
- `Theory/` – Includes theoretical explanations and resources related to opacity.
- `Website/` – Holds the complete website files showcasing the case study and scipts to easily host and test the websites

### File Overview

```
├── Testing/                 # Scripts and datasets for runtime measurement and simulation
    └── time_output.xlsx     # Final output timing data               
├── Theory/                  # Theoretical models used in the thesis       
├── Website/                 # Realistic case study web app
│   ├── Healthcare/          # Healthcare system
│   └── Parachute/           # Parachute system
├── runWebsites.py           # Backup script to launch both mock web apps simultaneously
├── README.md                # This file

```

| File / Script                    | Description                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| `runWebsites.py`                 | Backup script to launch both web servers through python (not recommended, see Setup).        |
| `health_server.py`               | Backend for the Healthcare system.                                                           |
| `para_server.py`                 | Backend for the Parachute system.                                                            |
| `index.html` (under each system) | Frontend interface for the respective case study applications.                               |
| `createBoxplot.py`               | Generates performance comparison plots from recorded timing data.                            |
| `Test_Website.py`                | Used to programmatically test server response and simulate client behavior.                  |
| `time_data.xlsx`, etc.           | Raw and filtered timing measurements for various caching strategies.                         |
| `boxplot_*.png`                  | Visual runtime comparisons between configurations (cached, no cache, etc.).                  |
| `Comparison Server.png`          | Summary visualization comparing systems.                                                     |
| `time_output.xlsx`               | Final formatted timing results, used in Table \ref{tab\:case\_study\_results} of the thesis. |

---

## 🛠️ Setup (Healthcare Site with Apache)

For a more detailed tutorial, see:

- [Apache Virtual Hosts Documentation](https://httpd.apache.org/docs/2.4/vhosts/)
- [DigitalOcean Apache Guide](https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-ubuntu-20-04)

but make sure to add our scripts, files and folders and update all paths and links accordingly

For a quick setup that uses python instead of Apache see Backup

To set up the case study:

### 1. Clone the repository

```bash
git clone https://github.com/MidanLP/Opacity-Case-Study.git
```

### 2. Copy Healthcare files into Apache directory

```bash
sudo mkdir -p /var/www/Healthcare
sudo cp -r Opacity-Case-Study/Website/Healthcare/* /var/www/Healthcare/
```

### 3. Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/Healthcare
sudo chmod -R 755 /var/www/Healthcare
```

### 4. Configure Apache to Listen on Port 8080

Edit:

```bash
sudo nano /etc/apache2/ports.conf
```

Ensure this line exists:

```apache
Listen 8080
```

### 5. Create the Virtual Host Config

```bash
sudo nano /etc/apache2/sites-available/healthcare.conf
```

Paste:

```apache
<VirtualHost *:8080>
    ServerName healthcare.local
    DocumentRoot /var/www/Healthcare

    <Directory /var/www/Healthcare>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/healthcare_error.log
    CustomLog ${APACHE_LOG_DIR}/healthcare_access.log combined
</VirtualHost>
```

### 6. Enable the Site and Restart Apache

```bash
sudo a2ensite healthcare.conf
sudo systemctl restart apache2
```

### Backup 
```
python .\Website\runWebsites.py    
```

## 📂 Dependencies

Make sure the following are installed:

- Python 3+
- `pandas`
- `selenium`
- `matplotlib`
- `webdriver-manager` (ChromeDriverManager)

---

## 🧰 Testing

1. Ensure all dependencies are installed.
2. Navigate to the `Testing` folder.
3. Open `Test_Website.py` and adjust:
   - Paths to correct locations
   - Link to Healthcare image (e.g. `http://localhost:8081/parachute.jpeg`)
4. Run the script:

```bash
python Test_Website.py
```

5. Input number of test runs (default: 1)
6. Input `yes/no` to clear cache between runs
7. View results in `time_output.xlsx`, sheet: `Testing Times`

---

