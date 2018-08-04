#!/bin/bash
# source ~/.bashrc
# actCom
source /home/anita/anaconda3/envs/commodity_data_analyzer/bin/activate commodity_data_analyzer
python /home/anita/commodity_data_analyzer/Bigbasket_scraping.py > /tmp/log_actual_scraper
source /home/anita/anaconda3/envs/commodity_data_analyzer/bin/deactivate
