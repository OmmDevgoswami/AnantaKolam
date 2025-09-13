import streamlit as st
from google import genai
from google.genai import types
import json
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Advanced Kolam Generator", layout="wide")
st.title("🎨 AI-Powered Kolam Generator - Beautiful & Colorful Designs")

# -----------------------------
# API Key Setup
# -----------------------------
# Direct API key integration
api_key = "AIzaSyBMThlSDjHMjrCsfxu8bjUZ8VBkDkCYKHg"
genai.configure(api_key=api_key)

# -----------------------------
# Advanced Kolam Prompt Templates
# -----------------------------
# Enhanced AI prompt with specific color instructions
def create_advanced_kolam_prompt(kolam_type, state, complexity, grid_size, color_scheme, occasion, custom_elements):
    """Create structured Kolam generation prompt (JSON format)"""
    prompt = """
    {
        "kolam_design": {
            "name": "Name of the kolam design (e.g., '1-3-5-7-9-7-5-3-1 Parallel dots')",
            "origin": {
                "region": "South India",
                "state": "Tamil Nadu"
                },
                [cite_start]"description": "A brief description of the design and its cultural significance[cite: 4, 5, 17].",
                "dot_grid": {
                    [cite_start]"type": "The arrangement of the dots (pulli) (e.g., 'square', 'stepped', 'free shape') [cite: 21, 22, 57, 72]",
                    "dimensions": {
                        [cite_start]"square_grid_size": "For square grids, the n x n dimension (e.g., 5) [cite: 190]",
                        [cite_start]"stepped_grid_center_row": "For stepped grids, the number of dots in the center row (e.g., 5 or 9) [cite: 192, 193]",
                        [cite_start]"total_pulli": "The total number of dots in the design [cite: 187]"
                        },
                        "mathematical_formulas": {
                            [cite_start]"square_grid_total_pulli": "n * n or n^2 [cite: 191]",
                            [cite_start]"stepped_grid_total_pulli": "2*((n-1)/2)^2 + n [cite: 211]"
                            }
                            },
                            "kambi_line": {
                                [cite_start]"path_type": "Classification of the line drawing (e.g., 'single loop', 'multiple loops') [cite: 48, 79]",
                                [cite_start]"graph_theory_model": "Graph theory concept that applies (e.g., 'Eulerian path', 'Eulerian circuit', 'Hamiltonian Cycle', 'Traveling Salesman Problem') [cite: 51, 115, 116]",
                                "line_properties": {
                                    [cite_start]"lines": "Type of lines used ('linear' or 'curvilinear') [cite: 21, 22]",
                                    "stroke_continuity": "Is the drawing completed with a single, uninterrupted line? (boolean) [cite_start][cite: 22, 25]"
                                    }
                                    },
                                    "geometric_properties": {
                                        "symmetry": {
                                            [cite_start]"type": "Type of symmetry present ('reflectional', 'rotational', 'both', 'none') [cite: 31, 34, 146, 159]",
                                            [cite_start]"lines_of_reflection": "Number of lines of reflection symmetry [cite: 145]",
                                            [cite_start]"angle_of_rotation": "Smallest angle of rotational symmetry in degrees [cite: 145]"
                                            },
                                            "pattern_rules": [
                                                "A list of rules followed, as deduced by Yanagisawa and Nagata and others:",
                                                [cite_start]"Loop drawing-lines, and never trace a line through the same route[cite: 24].",
                                                [cite_start]"The drawing is completed when all points are enclosed by a drawing-line[cite: 25].",
                                                [cite_start]"Straight lines are drawn along the dual grid inclined at an angle of 45 degrees[cite: 26].",
                                                [cite_start]"Arcs are drawn surrounding the points[cite: 27].",
                                                [cite_start]"There must be symmetry in the drawings[cite: 31]."
                                                ]
                                                },
                                                "analysis_results": {
                                                    "has_euler_path": "Does the design contain an Euler path? (boolean) [cite_start][cite: 115]"
                                                    "has_euler_circuit": "Does the design contain an Euler circuit? (boolean) [cite_start][cite: 116]",
                                                    "justification": "Explanation based on the number of odd vertices. [cite_start]If a graph has exactly two odd vertices, it has an Euler path[cite: 161]. [cite_start]If all vertices are even, it has an Euler path and an Euler circuit[cite: 156].
                                                    },
                                                    [cite_start]"extensibility": "Description of how the pattern can be extended (e.g., 'by increasing the number of dots') [cite: 78, 79, 251]",
                                                    "cultural_context": {
                                                        [cite_start]"purpose": "Decoration, a daily tribute to harmonious co-existence, a welcoming sign to all beings including the Goddess Lakshmi [cite: 17, 19, 20]",
                                                        [cite_start]"materials": "White rice powder, powdered white stone, diluted rice paste, cow dung [cite: 11, 15, 18, 168, 169, 171]",
                                                        [cite_start]"process": "Drawn daily in the morning on a cleaned and dampened surface [cite: 11, 13, 170]",
                                                        [cite_start]"artisans": "Typically drawn by women [cite: 11, 36, 37]"
                                                        }
                                                        }
                                                        }
                                                        """
    return prompt

    """Create sophisticated prompts for stunning Kolam generation with guaranteed colors"""
    
    # Specific color palettes for each scheme
    color_palettes = {
        "Vibrant Festival": {
            "background": "#2C1810",
            "primary": ["#FF6B35", "#FFD23F", "#06FFA5", "#FF1744"],
            "accent": ["#E91E63", "#9C27B0"]
        },
        "Royal Colors": {
            "background": "#1A1A2E", 
            "primary": ["#FFD700", "#4A148C", "#B71C1C", "#FF6F00"],
            "accent": ["#1A237E", "#4A148C"]
        },
        "Pastel Dream": {
            "background": "#F8F8FF",
            "primary": ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA"],
            "accent": ["#E1BAFF", "#FFB3E6"]
        },
        "Nature Inspired": {
            "background": "#2E4057",
            "primary": ["#8BC34A", "#FF9800", "#2196F3", "#FFC107"],
            "accent": ["#795548", "#607D8B"]
        },
        "Traditional White": {
            "background": "#1C1C1C",
            "primary": ["#FFFFFF", "#F5F5F5", "#E0E0E0", "#BDBDBD"],
            "accent": ["#9E9E9E", "#757575"]
        },
        "Monochrome Elegant": {
            "background": "#000000",
            "primary": ["#FFFFFF", "#BDBDBD", "#757575", "#424242"],
            "accent": ["#9E9E9E", "#616161"]
        }
    }
    
    selected_palette = color_palettes.get(color_scheme, color_palettes["Vibrant Festival"])
    
    prompt = f"""
    Create a stunning, highly detailed {kolam_type} design representing {state} tradition.
    
    MANDATORY COLOR REQUIREMENTS - MUST BE INCLUDED:
    {{
        "visual_elements": {{
            "background_color": "{selected_palette['background']}",
            "primary_colors": {selected_palette['primary']},
            "accent_colors": {selected_palette['accent']}
        }},
        "pattern_structure": {{
            "central_motif": {{
                "type": "lotus",
                "position": [400, 400],
                "size": 80,
                "colors": ["{selected_palette['primary'][0]}", "{selected_palette['primary'][1]}"]
            }},
            "border_patterns": [
                {{
                    "pattern": "floral",
                    "thickness": 40,
                    "colors": ["{selected_palette['primary'][2]}", "{selected_palette['accent'][0]}"]
                }}
            ],
            "corner_elements": [
                {{
                    "position": "all_corners",
                    "size": 25,
                    "colors": ["{selected_palette['accent'][1]}"]
                }}
            ],
            "connecting_patterns": [
                {{
                    "type": "radiating_lines",
                    "color": "{selected_palette['primary'][1]}",
                    "width": 3
                }}
            ],
            "decorative_fills": [
                {{
                    "type": "geometric_rings",
                    "colors": {selected_palette['primary'][:3]},
                    "opacity": 0.8
                }}
            ]
        }},
        "design_info": {{
            "name": "Beautiful {kolam_type} from {state}",
            "description": "A vibrant and intricate {kolam_type} featuring traditional {state} motifs with {color_scheme.lower()} colors, perfect for {occasion.lower()}",
            "cultural_meaning": "Traditional {state} kolam symbolizing prosperity, beauty, and spiritual harmony",
            "difficulty": "{complexity}",
            "estimated_time": "45-60 minutes"
        }},
        "step_by_step_guide": [
            "Start by preparing the {selected_palette['background']} background surface",
            "Draw the central lotus motif using {selected_palette['primary'][0]} and {selected_palette['primary'][1]} colors",
            "Add decorative borders with {selected_palette['primary'][2]} colored patterns",
            "Fill in corner elements using {selected_palette['accent'][0]} accent color",
            "Connect all elements with {selected_palette['primary'][1]} radiating lines",
            "Add final decorative touches and color gradients for depth"
        ],
        "pro_tips": [
            "Use {color_scheme.lower()} color palette for authentic {state} style",
            "Blend colors gently for smooth transitions between {selected_palette['primary'][0]} and {selected_palette['primary'][1]}",
            "Ensure symmetry in all four directions for traditional kolam balance",
            "Layer colors from light to dark for better visual depth"
        ],
        "color_mixing_guide": {{
            "primary_mix": "Blend {selected_palette['primary'][0]} with {selected_palette['primary'][1]} for smooth gradients",
            "gradients": "Create transitions between all primary colors: {', '.join(selected_palette['primary'])}",
            "highlights": "Use {selected_palette['accent'][0]} for emphasis and {selected_palette['accent'][1]} for shadows"
        }}
    }}
    
    ADDITIONAL REQUIREMENTS:
    - Grid Size: {grid_size}x{grid_size} underlying structure
    - Complexity: {complexity} level with appropriate detail density
    - Special Elements: {custom_elements if custom_elements else 'Traditional lotus and peacock motifs'}
    - Cultural Style: Authentic {state} regional patterns and symbolism
    - Occasion: Designed specifically for {occasion} celebrations
    
    CRITICAL: Return EXACTLY the JSON structure above with all the specified colors. The visual_elements section with background_color, primary_colors, and accent_colors is MANDATORY and must match the {color_scheme} palette exactly.
    """
    
    return prompt

# -----------------------------
# Advanced Visualization Functions
# -----------------------------
def create_stunning_kolam_visualization(kolam_data, canvas_size=800):
    """Create beautiful, colorful kolam visualizations"""
    
    # Set up the figure with high DPI for crisp output
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=100)
    ax.set_xlim(0, canvas_size)
    ax.set_ylim(0, canvas_size)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Set background color
    bg_color = kolam_data.get('visual_elements', {}).get('background_color', '#000000')
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    pattern_structure = kolam_data.get('pattern_structure', {})
    
    # Draw central motif
    central_motif = pattern_structure.get('central_motif', {})
    if central_motif:
        draw_central_motif(ax, central_motif, canvas_size)
    
    # Draw borders
    for border in pattern_structure.get('border_patterns', []):
        draw_border_pattern(ax, border, canvas_size)
    
    # Draw corner elements
    for corner in pattern_structure.get('corner_elements', []):
        draw_corner_element(ax, corner, canvas_size)
    
    # Draw connecting patterns
    for pattern in pattern_structure.get('connecting_patterns', []):
        draw_connecting_pattern(ax, pattern, canvas_size)
    
    # Draw decorative fills
    for fill in pattern_structure.get('decorative_fills', []):
        draw_decorative_fill(ax, fill, canvas_size)
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', 
                facecolor=bg_color, dpi=150, pad_inches=0.1)
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)
    
    return img

def draw_central_motif(ax, motif, canvas_size):
    """Draw the central motif (lotus, mandala, etc.)"""
    center_x = motif.get('position', [canvas_size//2, canvas_size//2])[0]
    center_y = motif.get('position', [canvas_size//2, canvas_size//2])[1]
    size = motif.get('size', 50)
    colors = motif.get('colors', ['#FFD700', '#FF6B6B'])
    motif_type = motif.get('type', 'mandala')
    
    if motif_type == 'lotus':
        # Draw lotus petals
        for i in range(8):
            angle = i * 45
            petal = patches.Ellipse((center_x + size * np.cos(np.radians(angle)) * 0.3,
                                   center_y + size * np.sin(np.radians(angle)) * 0.3),
                                   size * 0.8, size * 0.3, angle=angle,
                                   facecolor=colors[0], alpha=0.8, edgecolor=colors[1], linewidth=2)
            ax.add_patch(petal)
        
        # Center circle
        center_circle = Circle((center_x, center_y), size * 0.2, 
                              facecolor=colors[1], edgecolor='white', linewidth=3)
        ax.add_patch(center_circle)
    
    elif motif_type == 'mandala':
        # Draw mandala pattern
        for radius in [size * 0.8, size * 0.6, size * 0.4, size * 0.2]:
            circle = Circle((center_x, center_y), radius, 
                           fill=False, edgecolor=colors[0], linewidth=3, alpha=0.8)
            ax.add_patch(circle)
            
            # Add spokes
            for i in range(12):
                angle = i * 30
                x_end = center_x + radius * np.cos(np.radians(angle))
                y_end = center_y + radius * np.sin(np.radians(angle))
                ax.plot([center_x, x_end], [center_y, y_end], 
                       color=colors[1], linewidth=2, alpha=0.7)

def draw_border_pattern(ax, border, canvas_size):
    """Draw decorative borders"""
    thickness = border.get('thickness', 20)
    colors = border.get('colors', ['#4CAF50', '#2196F3'])
    pattern_type = border.get('pattern', 'geometric')
    
    # Outer border rectangle
    border_rect = patches.Rectangle((thickness//2, thickness//2), 
                                   canvas_size - thickness, canvas_size - thickness,
                                   fill=False, edgecolor=colors[0], linewidth=thickness//2)
    ax.add_patch(border_rect)
    
    # Add decorative elements along border
    if pattern_type == 'floral':
        for i in range(0, canvas_size, 60):
            if i > thickness and i < canvas_size - thickness:
                # Top border flowers
                flower = Circle((i, canvas_size - thickness//2), thickness//4,
                               facecolor=colors[1], alpha=0.7)
                ax.add_patch(flower)
                # Bottom border flowers
                flower = Circle((i, thickness//2), thickness//4,
                               facecolor=colors[1], alpha=0.7)
                ax.add_patch(flower)
                # Left border flowers
                flower = Circle((thickness//2, i), thickness//4,
                               facecolor=colors[1], alpha=0.7)
                ax.add_patch(flower)
                # Right border flowers
                flower = Circle((canvas_size - thickness//2, i), thickness//4,
                               facecolor=colors[1], alpha=0.7)
                ax.add_patch(flower)

def draw_corner_element(ax, corner, canvas_size):
    """Draw corner decorative elements"""
    position = corner.get('position', 'top_left')
    size = corner.get('size', 30)
    colors = corner.get('colors', ['#E91E63'])
    
    corner_positions = {
        'top_left': (size, canvas_size - size),
        'top_right': (canvas_size - size, canvas_size - size),
        'bottom_left': (size, size),
        'bottom_right': (canvas_size - size, size)
    }
    
    x, y = corner_positions.get(position, corner_positions['top_left'])
    
    # Draw decorative corner element
    corner_element = Circle((x, y), size, facecolor=colors[0], alpha=0.6)
    ax.add_patch(corner_element)
    
    # Add inner detail
    inner_circle = Circle((x, y), size * 0.5, facecolor='white', alpha=0.8)
    ax.add_patch(inner_circle)

def draw_connecting_pattern(ax, pattern, canvas_size):
    """Draw connecting lines and curves"""
    path = pattern.get('path', [])
    color = pattern.get('color', '#FFFFFF')
    width = pattern.get('width', 2)
    
    if len(path) >= 2:
        x_coords = [point[0] for point in path]
        y_coords = [point[1] for point in path]
        ax.plot(x_coords, y_coords, color=color, linewidth=width, alpha=0.8)

def draw_decorative_fill(ax, fill, canvas_size):
    """Draw filled decorative areas"""
    area = fill.get('area', [])
    colors = fill.get('colors', ['#FFC107'])
    opacity = fill.get('opacity', 0.5)
    
    if len(area) >= 3:
        polygon = Polygon(area, facecolor=colors[0], alpha=opacity, edgecolor='white')
        ax.add_patch(polygon)

# -----------------------------
# Streamlit Interface
# -----------------------------
st.sidebar.header("🎨 Kolam Design Studio")

# Enhanced input options
col1, col2 = st.sidebar.columns(2)

with col1:
    kolam_type = st.selectbox(
        "Kolam Style",
        ["Sikku Kolam", "Pulli Kolam", "Rangoli", "Freehand Kolam", 
         "Geometric Kolam", "Floral Kolam", "Festival Special"],
        index=2
    )
    
    state = st.selectbox(
        "Regional Style",
        ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Kerala", "Telangana"]
    )

with col2:
    complexity = st.selectbox(
        "Complexity",
        ["Beginner", "Intermediate", "Advanced", "Master Level"],
        index=1
    )
    
    grid_size = st.slider("Pattern Density", 8, 20, 12)

# Color scheme with preview
color_scheme = st.sidebar.selectbox(
    "Color Theme",
    ["Vibrant Festival", "Royal Colors", "Pastel Dream", 
     "Nature Inspired", "Traditional White", "Monochrome Elegant"]
)

# Show color palette preview
color_palettes = {
    "Vibrant Festival": ["#FF6B35", "#F7931E", "#FFD23F", "#06FFA5", "#B19CD9"],
    "Royal Colors": ["#4A148C", "#FFD700", "#1A237E", "#B71C1C", "#FF6F00"],
    "Pastel Dream": ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#E1BAFF"],
    "Nature Inspired": ["#8BC34A", "#FF9800", "#795548", "#2196F3", "#FFC107"],
    "Traditional White": ["#FFFFFF", "#F5F5F5", "#E0E0E0"],
    "Monochrome Elegant": ["#000000", "#424242", "#757575", "#BDBDBD", "#FFFFFF"]
}

if color_scheme in color_palettes:
    cols = st.sidebar.columns(len(color_palettes[color_scheme]))
    for i, color in enumerate(color_palettes[color_scheme]):
        with cols[i]:
            st.color_picker("", color, key=f"preview_{i}", disabled=True)

occasion = st.sidebar.selectbox(
    "Special Occasion",
    ["Daily Practice", "Diwali", "Pongal", "Wedding", "Navratri", "Housewarming"]
)

custom_elements = st.sidebar.text_area(
    "Custom Elements",
    placeholder="e.g., peacock motifs, lotus flowers, geometric spirals, temple architecture...",
    height=80
)

# Generate button
if st.sidebar.button("🎨 Create Stunning Kolam", type="primary", use_container_width=True):
    with st.spinner("🎭 AI is creating your masterpiece..."):
        try:
            # Generate advanced prompt
            advanced_prompt = create_advanced_kolam_prompt(
                kolam_type, state, complexity, grid_size, 
                color_scheme, occasion, custom_elements
            )
            
            # Call Gemini with enhanced prompt
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(
                advanced_prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.8,  # Higher creativity
                    "candidate_count": 1,
                    "max_output_tokens": 4000
                }
            )
            
            kolam_data = json.loads(response.text)
            
            # Display results in columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(f"✨ {kolam_data.get('design_info', {}).get('name', 'Beautiful Kolam')}")
                
                # Create beautiful visualization
                kolam_image = create_stunning_kolam_visualization(kolam_data)
                st.image(kolam_image, use_container_width=True, caption="Your AI-Generated Kolam Design")
                
                # Download button
                img_buffer = io.BytesIO()
                kolam_image.save(img_buffer, format='PNG', quality=95, dpi=(300, 300))
                st.download_button(
                    "📱 Download High-Quality Image",
                    img_buffer.getvalue(),
                    f"{kolam_type}_{state}_{complexity}.png",
                    "image/png",
                    use_container_width=True
                )
            
            with col2:
                design_info = kolam_data.get('design_info', {})
                
                st.info(f"**Description:** {design_info.get('description', 'A beautiful traditional design')}")
                
                if design_info.get('cultural_meaning'):
                    st.success(f"**Cultural Meaning:** {design_info['cultural_meaning']}")
                
                st.metric("Difficulty Level", design_info.get('difficulty', complexity))
                st.metric("Estimated Time", design_info.get('estimated_time', '30-45 minutes'))
                
                # Color guide
                visual_elements = kolam_data.get('visual_elements', {})
                if visual_elements.get('primary_colors'):
                    st.subheader("🎨 Color Palette")
                    color_cols = st.columns(3)
                    for i, color in enumerate(visual_elements['primary_colors'][:3]):
                        with color_cols[i % 3]:
                            st.color_picker("", color, key=f"color_{i}", disabled=True)
            
            # Instructions section
            st.markdown("---")
            col_inst1, col_inst2 = st.columns(2)
            
            with col_inst1:
                st.subheader("📋 Step-by-Step Guide")
                for i, step in enumerate(kolam_data.get('step_by_step_guide', []), 1):
                    st.write(f"**{i}.** {step}")
            
            with col_inst2:
                st.subheader("💡 Pro Tips")
                for tip in kolam_data.get('pro_tips', []):
                    st.write(f"• {tip}")
                
                color_guide = kolam_data.get('color_mixing_guide', {})
                if color_guide:
                    st.subheader("🎭 Color Mixing Guide")
                    for key, value in color_guide.items():
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Try simplifying your requirements or check the API connection.")

# Gallery section
st.markdown("---")
st.subheader("🖼️ Kolam Gallery & Inspiration")

gallery_cols = st.columns(3)
sample_designs = [
    {"name": "Festival Lotus", "style": "Floral", "colors": "Vibrant"},
    {"name": "Geometric Harmony", "style": "Geometric", "colors": "Royal"},
    {"name": "Traditional Elegance", "style": "Sikku", "colors": "Classic"}
]

for i, design in enumerate(sample_designs):
    with gallery_cols[i]:
        st.info(f"**{design['name']}**\nStyle: {design['style']}\nColors: {design['colors']}")

# Educational content
with st.expander("📚 Learn About Kolam Art"):
    st.write("""
    **Kolam** is a form of drawing that uses rice flour/chalk/chalk powder/white stone powder, often created during Indian festivals. 
    
    **Key Elements:**
    - **Symmetry**: Most kolams follow radial or bilateral symmetry
    - **Continuous Lines**: Sikku kolams are drawn without lifting the tool
    - **Sacred Geometry**: Many designs incorporate mathematical principles
    - **Cultural Symbolism**: Each motif has spiritual significance
    - **Seasonal Variations**: Designs change with festivals and seasons
    
    **Regional Variations:**
    - **Tamil Nadu**: Kolam - Rice flour patterns
    - **Karnataka**: Rangoli - Colorful geometric designs  
    - **Andhra Pradesh**: Muggu - Intricate dot-based patterns
    - **Kerala**: Pookalam - Flower-based circular arrangements
    """)

st.markdown("---")
st.caption("🎨 AI-Powered Kolam Generator - Bringing Traditional Art to Digital Life")