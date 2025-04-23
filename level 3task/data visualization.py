import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Data Visualization Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        self.df = None
        self.file_path = None
        self.selected_columns = []
        self.current_fig = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create frames
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)
        self.left_frame = tk.Frame(self.root, bg="#f0f0f0", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        self.right_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Top frame - File loading
        tk.Label(self.top_frame, text="Data File:", bg="#f0f0f0", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.file_path_var = tk.StringVar()
        tk.Entry(self.top_frame, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(self.top_frame, text="Browse", command=self.load_file, bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Left frame - Controls
        tk.Label(self.left_frame, text="Visualization Controls", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Visualization type
        tk.Label(self.left_frame, text="Visualization Type:", bg="#f0f0f0", font=("Arial", 12)).pack(anchor='w', padx=5, pady=5)
        self.viz_type = tk.StringVar(value="Scatter Plot")
        viz_types = ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot", "Heatmap", "Pie Chart", "3D Scatter"]
        viz_dropdown = ttk.Combobox(self.left_frame, textvariable=self.viz_type, values=viz_types, width=25)
        viz_dropdown.pack(anchor='w', padx=5, pady=2)
        
        # Library selection
        tk.Label(self.left_frame, text="Library:", bg="#f0f0f0", font=("Arial", 12)).pack(anchor='w', padx=5, pady=5)
        self.library = tk.StringVar(value="Matplotlib")  # Default to Matplotlib instead of Plotly
        lib_types = ["Matplotlib", "Seaborn", "Plotly (Static)"]  # Changed Plotly to "Plotly (Static)"
        lib_dropdown = ttk.Combobox(self.left_frame, textvariable=self.library, values=lib_types, width=25)
        lib_dropdown.pack(anchor='w', padx=5, pady=2)
        
        self.column_frame = tk.LabelFrame(self.left_frame, text="Data Columns", bg="#f0f0f0", font=("Arial", 12))
        self.column_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.column_listbox = tk.Listbox(self.column_frame, selectmode=tk.MULTIPLE, height=10, width=25)
        self.column_listbox.pack(padx=5, pady=5, fill=tk.X)
        
        self.settings_frame = tk.LabelFrame(self.left_frame, text="Plot Settings", bg="#f0f0f0", font=("Arial", 12))
        self.settings_frame.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Label(self.settings_frame, text="X-Axis:", bg="#f0f0f0").pack(anchor='w', padx=5, pady=2)
        self.x_axis = tk.StringVar()
        self.x_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.x_axis, width=20)
        self.x_dropdown.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(self.settings_frame, text="Y-Axis:", bg="#f0f0f0").pack(anchor='w', padx=5, pady=2)
        self.y_axis = tk.StringVar()
        self.y_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.y_axis, width=20)
        self.y_dropdown.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(self.settings_frame, text="Color By (Optional):", bg="#f0f0f0").pack(anchor='w', padx=5, pady=2)
        self.color_by = tk.StringVar()
        self.color_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.color_by, width=20)
        self.color_dropdown.pack(anchor='w', padx=5, pady=2)
        
        tk.Label(self.settings_frame, text="Plot Title:", bg="#f0f0f0").pack(anchor='w', padx=5, pady=2)
        self.plot_title = tk.StringVar(value="Data Visualization")
        tk.Entry(self.settings_frame, textvariable=self.plot_title, width=25).pack(anchor='w', padx=5, pady=2)
        
        tk.Button(self.left_frame, text="Generate Visualization", command=self.generate_visualization, 
                 bg="#007BFF", fg="white", font=("Arial", 12)).pack(pady=10, fill=tk.X, padx=5)
        
        tk.Button(self.left_frame, text="Save Visualization", command=self.save_visualization,
                 bg="#28a745", fg="white", font=("Arial", 12)).pack(pady=5, fill=tk.X, padx=5)
        
        self.canvas_frame = tk.Frame(self.right_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_var = tk.StringVar(value="Ready. Please load a dataset.")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_file(self):
        file_types = [
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("JSON files", "*.json"),
            ("All files", "*.*")
        ]
        self.file_path = filedialog.askopenfilename(title="Select Data File", filetypes=file_types)
        
        if self.file_path:
            try:
                self.file_path_var.set(self.file_path)
                file_ext = os.path.splitext(self.file_path)[1].lower()
                
                if file_ext == '.csv':
                    self.df = pd.read_csv(self.file_path)
                elif file_ext == '.xlsx':
                    self.df = pd.read_excel(self.file_path)
                elif file_ext == '.json':
                    self.df = pd.read_json(self.file_path)
                else:
                    raise ValueError("Unsupported file format")
                
                self.update_column_selection()
                self.status_var.set(f"Loaded dataset with {self.df.shape[0]} rows and {self.df.shape[1]} columns")
            except Exception as e:
                self.status_var.set(f"Error loading file: {str(e)}")
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def update_column_selection(self):
        self.column_listbox.delete(0, tk.END)
        
        columns = list(self.df.columns)
        for col in columns:
            self.column_listbox.insert(tk.END, col)
        
        self.x_dropdown['values'] = [""] + columns
        self.y_dropdown['values'] = [""] + columns
        self.color_dropdown['values'] = [""] + columns
        
        if len(columns) > 0:
            self.x_axis.set(columns[0])
            if len(columns) > 1:
                self.y_axis.set(columns[1])
            else:
                self.y_axis.set(columns[0])
            self.color_by.set("")
    
    def generate_visualization(self):
        if self.df is None:
            self.status_var.set("Please load a dataset first")
            messagebox.showwarning("Warning", "Please load a dataset first")
            return
        
        viz_type = self.viz_type.get()
        library = self.library.get()
        x_col = self.x_axis.get()
        y_col = self.y_axis.get()
        color_col = self.color_by.get() if self.color_by.get() != "" else None
        title = self.plot_title.get()
        
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            if library == "Plotly (Static)":
                self.generate_plotly_viz(viz_type, x_col, y_col, color_col, title)
            elif library == "Matplotlib":
                self.generate_matplotlib_viz(viz_type, x_col, y_col, color_col, title)
            elif library == "Seaborn":
                self.generate_seaborn_viz(viz_type, x_col, y_col, color_col, title)
            
            self.status_var.set(f"Generated {viz_type} using {library}")
        except Exception as e:
            self.status_var.set(f"Error generating visualization: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate visualization: {str(e)}")
    
    def generate_plotly_viz(self, viz_type, x_col, y_col, color_col, title):
        fig = None
        
        if viz_type == "Scatter Plot":
            fig = px.scatter(self.df, x=x_col, y=y_col, color=color_col, title=title)
        elif viz_type == "Line Chart":
            fig = px.line(self.df, x=x_col, y=y_col, color=color_col, title=title)
        elif viz_type == "Bar Chart":
            fig = px.bar(self.df, x=x_col, y=y_col, color=color_col, title=title)
        elif viz_type == "Histogram":
            fig = px.histogram(self.df, x=x_col, color=color_col, title=title)
        elif viz_type == "Box Plot":
            fig = px.box(self.df, x=x_col, y=y_col, color=color_col, title=title)
        elif viz_type == "Heatmap":
            if x_col and y_col and color_col:
                pivot_df = self.df.pivot_table(index=x_col, columns=y_col, values=color_col, aggfunc='mean')
                fig = px.imshow(pivot_df, title=title)
            else:
                corr_df = self.df.select_dtypes(include=[np.number]).corr()
                fig = px.imshow(corr_df, title=title or "Correlation Matrix")
        elif viz_type == "Pie Chart":
            fig = px.pie(self.df, names=x_col, values=y_col, title=title)
        elif viz_type == "3D Scatter":
            z_col = color_col 
            if z_col:
                fig = px.scatter_3d(self.df, x=x_col, y=y_col, z=z_col, title=title)
            else:
                self.status_var.set("3D Scatter requires a third column (set as Color)")
                messagebox.showwarning("Warning", "3D Scatter requires a third column (set as Color)")
                return
        
        self.current_fig = fig
        
                 plt.figure(figsize=(10, 6))     
        
        if viz_type == "3D Scatter":
            ax = plt.figure().add_subplot(111, projection='3d')
            ax.scatter(self.df[x_col], self.df[y_col], self.df[color_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_zlabel(color_col)
            ax.set_title(title)
        else:
            if viz_type == "Scatter Plot":
                plt.scatter(self.df[x_col], self.df[y_col])
            elif viz_type == "Line Chart":
                plt.plot(self.df[x_col], self.df[y_col])
            elif viz_type == "Bar Chart":
                plt.bar(self.df[x_col], self.df[y_col])
            elif viz_type == "Histogram":
                plt.hist(self.df[x_col], bins=20)
            elif viz_type == "Box Plot":
                self.df.boxplot(column=y_col, by=x_col)
            elif viz_type == "Heatmap":
                if x_col and y_col and color_col:
                    pivot_df = self.df.pivot_table(index=x_col, columns=y_col, values=color_col, aggfunc='mean')
                    plt.imshow(pivot_df)
                    plt.colorbar()
                else:
                    corr_df = self.df.select_dtypes(include=[np.number]).corr()
                    plt.imshow(corr_df)
                    plt.colorbar()
            elif viz_type == "Pie Chart":
                self.df.groupby(x_col)[y_col].sum().plot(kind='pie', autopct='%1.1f%%')
            
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f"{title} (Plotly Static Render)")
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        note_frame = tk.Frame(self.canvas_frame, bg="#f0f0f0")
        note_frame.pack(fill=tk.X)
        tk.Label(note_frame, text="Note: This is a static render of a Plotly visualization.", 
                 bg="#f0f0f0", fg="#555").pack(pady=5)
        
        tk.Button(note_frame, text="Save as Interactive HTML", 
                 command=lambda: self.save_as_html(), 
                 bg="#17a2b8", fg="white").pack(pady=5)
    
    def save_as_html(self):
        """Save the current Plotly figure as an interactive HTML file"""
        if hasattr(self, 'current_fig') and self.current_fig is not None:
            file_path = filedialog.asksaveasfilename(
                title="Save Interactive Visualization",
                filetypes=[("HTML files", "*.html")],
                defaultextension=".html"
            )
            
            if file_path:
                try:
                    self.current_fig.write_html(file_path)
                    self.status_var.set(f"Interactive visualization saved to {file_path}")
                    messagebox.showinfo("Success", 
                                       f"Interactive visualization saved to {file_path}\n\n"
                                       f"Open this file in your web browser to interact with the visualization.")
                except Exception as e:
                    self.status_var.set(f"Error saving HTML: {str(e)}")
                    messagebox.showerror("Error", f"Failed to save HTML: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No Plotly visualization available to save")
    
    def generate_matplotlib_viz(self, viz_type, x_col, y_col, color_col, title):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if viz_type == "Scatter Plot":
            if color_col:
                scatter = ax.scatter(self.df[x_col], self.df[y_col], c=self.df[color_col].astype('category').cat.codes)
                plt.colorbar(scatter, ax=ax, label=color_col)
            else:
                ax.scatter(self.df[x_col], self.df[y_col])
        elif viz_type == "Line Chart":
            if color_col:
                for category, group in self.df.groupby(color_col):
                    ax.plot(group[x_col], group[y_col], label=category)
                ax.legend()
            else:
                ax.plot(self.df[x_col], self.df[y_col])
        elif viz_type == "Bar Chart":
            if color_col:
                grouped = self.df.groupby([x_col, color_col])[y_col].mean().unstack()
                grouped.plot(kind='bar', ax=ax)
            else:
                self.df.groupby(x_col)[y_col].mean().plot(kind='bar', ax=ax)
        elif viz_type == "Histogram":
            ax.hist(self.df[x_col], bins=20)
        elif viz_type == "Box Plot":
            if color_col:
                self.df.boxplot(column=y_col, by=color_col, ax=ax)
            else:
                self.df.boxplot(column=y_col, ax=ax)
        elif viz_type == "Heatmap":
            if x_col and y_col and color_col:
                pivot_df = self.df.pivot_table(index=x_col, columns=y_col, values=color_col, aggfunc='mean')
                im = ax.imshow(pivot_df)
                plt.colorbar(im, ax=ax)
                ax.set_xticks(range(len(pivot_df.columns)))
                ax.set_yticks(range(len(pivot_df.index)))
                ax.set_xticklabels(pivot_df.columns)
                ax.set_yticklabels(pivot_df.index)
            else:
                corr_df = self.df.select_dtypes(include=[np.number]).corr()
                im = ax.imshow(corr_df)
                plt.colorbar(im, ax=ax)
                ax.set_xticks(range(len(corr_df.columns)))
                ax.set_yticks(range(len(corr_df.index)))
                ax.set_xticklabels(corr_df.columns, rotation=90)
                ax.set_yticklabels(corr_df.index)
        elif viz_type == "Pie Chart":
            self.df.groupby(x_col)[y_col].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
        elif viz_type == "3D Scatter":
            fig.clear()
            ax = fig.add_subplot(111, projection='3d')
            z_col = color_col
            if z_col:
                ax.scatter(self.df[x_col], self.df[y_col], self.df[z_col])
                ax.set_zlabel(z_col)
            else:
                self.status_var.set("3D Scatter requires a third column (set as Color)")
                messagebox.showwarning("Warning", "3D Scatter requires a third column (set as Color)")
                return
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)
        plt.tight_layout()
        
        self.current_fig = fig
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def generate_seaborn_viz(self, viz_type, x_col, y_col, color_col, title):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if viz_type == "Scatter Plot":
            sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=color_col, ax=ax)
        elif viz_type == "Line Chart":
            sns.lineplot(data=self.df, x=x_col, y=y_col, hue=color_col, ax=ax)
        elif viz_type == "Bar Chart":
            sns.barplot(data=self.df, x=x_col, y=y_col, hue=color_col, ax=ax)
        elif viz_type == "Histogram":
            sns.histplot(data=self.df, x=x_col, hue=color_col, ax=ax)
        elif viz_type == "Box Plot":
            sns.boxplot(data=self.df, x=x_col, y=y_col, hue=color_col, ax=ax)
        elif viz_type == "Heatmap":
            if x_col and y_col and color_col:
                pivot_df = self.df.pivot_table(index=x_col, columns=y_col, values=color_col, aggfunc='mean')
                sns.heatmap(pivot_df, annot=True, cmap="YlGnBu", ax=ax)
            else:
                corr_df = self.df.select_dtypes(include=[np.number]).corr()
                sns.heatmap(corr_df, annot=True, cmap="coolwarm", ax=ax)
        elif viz_type == "Pie Chart":
            self.df.groupby(x_col)[y_col].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
        elif viz_type == "3D Scatter":
            fig.clear()
            ax = fig.add_subplot(111, projection='3d')
            z_col = color_col
            if z_col:
                ax.scatter(self.df[x_col], self.df[y_col], self.df[z_col])
                ax.set_zlabel(z_col)
            else:
                self.status_var.set("3D Scatter requires a third column (set as Color)")
                messagebox.showwarning("Warning", "3D Scatter requires a third column (set as Color)")
                return
        
        ax.set_title(title)
        plt.tight_layout()
        
        self.current_fig = fig
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_visualization(self):
        if not hasattr(self, 'current_fig') or self.current_fig is None:
            self.status_var.set("No visualization to save. Generate one first.")
            messagebox.showinfo("Info", "No visualization to save. Generate one first.")
            return
        
        file_types = [
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("PDF Document", "*.pdf"),
            ("SVG Image", "*.svg")
        ]
        
        save_path = filedialog.asksaveasfilename(
            title="Save Visualization",
            filetypes=file_types,
            defaultextension=".png"
        )
        
        if save_path:
            try:
                self.current_fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.status_var.set(f"Visualization saved to {save_path}")
                messagebox.showinfo("Success", f"Visualization saved to {save_path}")
            except Exception as e:
                self.status_var.set(f"Error saving visualization: {str(e)}")
                messagebox.showerror("Error", f"Failed to save visualization: {str(e)}")

def create_sample_data():
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [10000, 12000, 9000, 15000, 11000, 13500],
        'Expenses': [8000, 7500, 9500, 8500, 9000, 9200],
        'Profit': [2000, 4500, -500, 6500, 2000, 4300],
        'Category': ['A', 'B', 'A', 'C', 'B', 'C']
    }
    
    df = pd.DataFrame(data)
    sample_file = "sample_data.csv"
    df.to_csv(sample_file, index=False)
    print(f"Sample data created at {os.path.abspath(sample_file)}")
    return sample_file

if __name__ == "__main__":
    try:
        
        root = tk.Tk()
        app = DataVisualizationTool(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        input("Press Enter to exit...")