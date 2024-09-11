# 🎓 Thesis Web App

### Created by **Marko Boreta**

Welcome to the repository of my **Fake News Detector Web App**! This project is a web application built using **Flask** and **jQuery**, and it leverages **Machine Learning Models** for fake news detction. The training and data analysis methodologies are documented in the notebooks available in the `training` folder.

🚀 The app uses **Docker** to run containers as part of a microservice architecture with **Docker Compose**.

---

## 🛠️ Installation & Setup

To get the web app up and running, follow these steps:

1. **Clone the Repository**  
   First, clone this repository to your local machine.
   
   \`\`\`bash
   git clone <repository-url>
   \`\`\`

2. **Navigate to the Services Folder**  
   Move into the `services` directory:
   
   \`\`\`bash
   cd services
   \`\`\`

3. **Ensure Docker is Installed** 🐳  
   Make sure you have **Docker** installed on your system. If not, you can download it [here](https://www.docker.com/products/docker-desktop).

4. **Build the Docker Containers** 🏗️  
   Now, run the following command to build the Docker containers:

   \`\`\`bash
   docker-compose build
   \`\`\`

5. **Run the Application** 🚀  
   Once the build is complete, start the application with:

   \`\`\`bash
   docker-compose up
   \`\`\`

6. **Access the Web App** 🌐  
   The app will be accessible at `http://localhost:5000` by default. Open your browser and start exploring the features!

---

## 📂 Folder Structure

Here’s a quick overview of the important folders in the repository:

- **`services/`** - Contains the Docker services for the app.
- **`training/`** - Includes all the training notebooks and data analysis methodologies.
- **`app/`** - Holds the Flask app's source code and configuration.

---

## 🧠 Machine Learning Integration

This web app integrates **Machine Learning Models** to provide intelligent insights and predictions. You can find all the training and data analysis materials in the `training` folder, where I’ve documented the methodologies used to train these models.
Three models have been used, **Naive Bayes**, **Passive Agressive Classifier** and **Logisitc Regression**.
---

## 📦 Microservices Architecture

The application is structured using a **microservices architecture**. Each component runs in its own container, ensuring scalability and modularity.

- **Flask**: Web framework to serve the frontend, each model and welcoming page are containarized and can communiczte with each other.
- **Machine Learning Models**: Backend models for predictions and analysis.

All services are managed through **Docker Compose**.

---

## 🌟 Features

- **🚀 Easy Setup with Docker**: Just clone, build, and run.
- **🧠 Machine Learning Models**: Integrated ML models for advanced functionality.
- **📈 Data Analysis**: Detailed analysis methodologies and notebooks.
- **🌐 Web Interface**: Interactive UI built with Flask and jQuery.

---

## 📝 Future Improvements

- Improve model accuracy.
- Add more detailed documentation on the model training process.
- Implement user authentication for secure access.

---

## 🔧 Troubleshooting

Having issues? Here are some common fixes:

- **Docker Build Errors**: Ensure Docker is installed correctly and try rebuilding the containers.
- **Accessing the App**: If the app isn’t running on `localhost:5000`, check your Docker logs for any issues.

---

## 👨‍💻 Author

**Marko Boreta**  
[LinkedIn](https://www.linkedin.com/in/marko-boreta-9b63a4268/)
