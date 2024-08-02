// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::api::process::{Command};

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
fn run_python_app() {
    let output = Command::new_sidecar("python-app")
        .expect("failed to create sidecar command")
        .output()
        .expect("failed to spawn sidecar command");

    if output.status.success() {
        println!("stdout: {}", output.stdout);
    } else {
        println!("stderr: {}", output.stderr);
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, run_python_app])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
