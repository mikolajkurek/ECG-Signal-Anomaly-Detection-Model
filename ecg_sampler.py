#!/usr/bin/env python3
"""
Simple ECG Sample Creator
Quick utility to create balanced ECG sample datasets
"""

import pandas as pd
import numpy as np
import sys

def show_help():
    """Show usage help."""
    print("ECG Sample Creator - Usage Examples:")
    print("=====================================")
    print()
    print("1. Create 100 samples with ALL labels equally distributed:")
    print("   python3 ecg_sampler.py")
    print()
    print("2. Create 100 samples with SPECIFIC labels:")
    print("   python3 ecg_sampler.py --labels 0 2 4")
    print()
    print("3. Create custom number of samples:")
    print("   python3 ecg_sampler.py --samples 50")
    print()
    print("4. Custom output filename:")
    print("   python3 ecg_sampler.py --output my_samples.csv")
    print()
    print("5. Show available labels:")
    print("   python3 ecg_sampler.py --show-labels")
    print()
    print("ECG Label Types:")
    print("  0.0 = Normal heartbeat")
    print("  1.0 = Supraventricular premature beat")
    print("  2.0 = Premature ventricular contraction")
    print("  3.0 = Fusion of ventricular beat")
    print("  4.0 = Unknown beat type")

def show_labels():
    """Show available labels in training data."""
    try:
        df_train = pd.read_csv('mitbih_train.csv')
        labels = df_train.iloc[:, -1]
        label_counts = labels.value_counts().sort_index()
        
        print("Available ECG Labels:")
        print("====================")
        label_descriptions = {
            0.0: "Normal heartbeat",
            1.0: "Supraventricular premature beat", 
            2.0: "Premature ventricular contraction",
            3.0: "Fusion of ventricular beat",
            4.0: "Unknown beat type"
        }
        
        for label, count in label_counts.items():
            percentage = (count / len(df_train)) * 100
            desc = label_descriptions.get(label, "Unknown")
            print(f"  {label}: {count:,} samples ({percentage:.2f}%) - {desc}")
        
        print(f"\nTotal training samples: {len(df_train):,}")
        
    except Exception as e:
        print(f"Error reading training data: {e}")

def create_samples(total_samples=100, include_labels=None, output_file='sample_mitbih.csv'):
    """Create balanced sample dataset."""
    try:
        print(f"Creating {total_samples} samples...")
        
        # Read training data
        df_train = pd.read_csv('mitbih_train.csv')
        available_labels = sorted(df_train.iloc[:, -1].unique())
        
        # Determine target labels
        if include_labels:
            target_labels = [label for label in include_labels if label in available_labels]
            if not target_labels:
                print("Error: None of the specified labels found in training data")
                return False
        else:
            target_labels = available_labels
        
        print(f"Using labels: {target_labels}")
        
        # Calculate distribution
        samples_per_label = total_samples // len(target_labels)
        remaining = total_samples % len(target_labels)
        
        # Collect samples
        selected_samples = []
        actual_total = 0
        
        for i, label in enumerate(target_labels):
            label_data = df_train[df_train.iloc[:, -1] == label].copy()
            
            current_samples = samples_per_label
            if i < remaining:
                current_samples += 1
                
            if len(label_data) < current_samples:
                print(f"Warning: Only {len(label_data)} samples available for label {label}")
                selected = label_data.copy()
            else:
                selected = label_data.sample(n=current_samples, random_state=42)
            
            selected_samples.append(selected)
            actual_total += len(selected)
            print(f"  Label {label}: {len(selected)} samples")
        
        # Combine and shuffle
        final_dataset = pd.concat(selected_samples, ignore_index=True)
        final_dataset = final_dataset.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save
        final_dataset.to_csv(output_file, index=False, header=False)
        
        print(f"\n✅ Created {len(final_dataset)} samples in '{output_file}'")
        print(f"Features per sample: {final_dataset.shape[1] - 1}")
        
        # Show final distribution
        final_labels = final_dataset.iloc[:, -1]
        label_counts = final_labels.value_counts().sort_index()
        print("Distribution:")
        for label, count in label_counts.items():
            percentage = (count / len(final_dataset)) * 100
            print(f"  Label {label}: {count} samples ({percentage:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function with argument parsing."""
    args = sys.argv[1:]
    
    # Default values
    total_samples = 100
    include_labels = None
    output_file = 'sample_mitbih.csv'
    
    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ['--help', '-h']:
            show_help()
            return
        elif arg == '--show-labels':
            show_labels()
            return
        elif arg == '--samples':
            if i + 1 < len(args):
                try:
                    total_samples = int(args[i + 1])
                    i += 1
                except ValueError:
                    print("Error: --samples requires a number")
                    return
        elif arg == '--labels':
            labels = []
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                try:
                    labels.append(float(args[i]))
                    i += 1
                except ValueError:
                    break
            if labels:
                include_labels = labels
            else:
                print("Error: --labels requires at least one label number")
                return
            i -= 1  # Adjust for outer loop increment
        elif arg == '--output':
            if i + 1 < len(args):
                output_file = args[i + 1]
                i += 1
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
            return
        
        i += 1
    
    # Create samples
    success = create_samples(total_samples, include_labels, output_file)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
