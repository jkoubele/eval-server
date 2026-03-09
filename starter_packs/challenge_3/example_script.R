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

n <- input_data$n  # number of Beyeronians


# Your code goes here
# Pro tip: you can use gmp package to represent large integers, that would otherwise overflow to inf:
# library(gmp)
# x <- as.bigz("123456789012345678901234567890")

result <- 42  # Replace with your computed result
# If you used bigz to represent to result, please convert it to string:
# result = as.character(result)

write_json(list(result = result), args$output_json, auto_unbox = TRUE)