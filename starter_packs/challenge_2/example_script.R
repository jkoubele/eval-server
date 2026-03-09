#!/usr/bin/env Rscript

library(argparse)
library(jsonlite)

parser <- ArgumentParser()

parser$add_argument(
  "--input_json",
  default = "./test_input_1.json", # You can change to test different input data, or provide via CLI
  help = "Path to input JSON"
)

parser$add_argument(
  "--output_json",
  default = "./output.json",
  help = "Path to output JSON" # You can optionally change the default if you want, or provide via CLI
)

args <- parser$parse_args()

input_data <- fromJSON(args$input_json)

num_halls <- input_data$num_halls
existing_tunnels <- input_data$existing_tunnels
potential_tunnels <- input_data$potential_tunnels

# Your code goes here
result <- 42  # Replace with your computed result (minimum cost needed to connect all halls)

write_json(list(result = result), args$output_json, auto_unbox = TRUE)
