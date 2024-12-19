# 1. Use ubuntu as base
FROM ubuntu:22.04

# 2. Install git
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean

# 3. Clone the app repo
WORKDIR /app
RUN git clone -b develop https://github.com/mihaiBront/CloudComputing_FinalProject.git .

# 4. Run script to create environment for the app
RUN bash -c "source .scripts/env-setup_deploy.bash"

# 5. Expose the port
EXPOSE 5000

# 6. Command for starting the app with container
CMD ["/bin/bash", "-c", "source .venv/bin/activate && flask run --host=0.0.0.0 --port=5000"]
