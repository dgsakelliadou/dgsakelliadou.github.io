"""
Generate an animated manifold GIF similar to geodesic flow visualizations
This creates a rotating 3D manifold with flow lines and color gradients
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

# Set up the figure with transparent background
fig = plt.figure(figsize=(10, 10), facecolor='white')
ax = fig.add_subplot(111, projection='3d', facecolor='white')

def create_manifold_with_geodesics(frame):
    """Create a manifold surface with geodesic flow lines"""
    ax.clear()
    
    # Create base manifold (torus-like surface)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, 2 * np.pi, 100)
    U, V = np.meshgrid(u, v)
    
    # Parameters for the manifold shape
    R = 2.5  # Major radius
    r = 1.0  # Minor radius
    
    # Create the surface with some modulation
    X = (R + r * np.cos(V) * (1 + 0.1 * np.cos(3 * U))) * np.cos(U)
    Y = (R + r * np.cos(V) * (1 + 0.1 * np.cos(3 * U))) * np.sin(U)
    Z = r * np.sin(V) * (1 + 0.1 * np.sin(2 * U))
    
    # Color based on curvature-like measure
    colors = np.sqrt(X**2 + Y**2 + Z**2)
    
    # Plot the manifold surface
    surf = ax.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(colors/colors.max()),
                          alpha=0.6, linewidth=0, antialiased=True,
                          shade=True)
    
    # Add geodesic flow lines
    num_geodesics = 12
    for i in range(num_geodesics):
        t = np.linspace(0, 4 * np.pi, 200)
        phase = (frame * 0.05 + i * 2 * np.pi / num_geodesics)
        
        # Geodesic parametrization
        u_geo = t + phase
        v_geo = 0.3 * np.sin(2 * t) + np.pi/2
        
        # Points on the geodesic
        X_geo = (R + r * np.cos(v_geo) * (1 + 0.1 * np.cos(3 * u_geo))) * np.cos(u_geo)
        Y_geo = (R + r * np.cos(v_geo) * (1 + 0.1 * np.cos(3 * u_geo))) * np.sin(u_geo)
        Z_geo = r * np.sin(v_geo) * (1 + 0.1 * np.sin(2 * u_geo))
        
        # Color the geodesic based on position
        colors_geo = plt.cm.plasma(i / num_geodesics)
        ax.plot(X_geo, Y_geo, Z_geo, color=colors_geo, linewidth=2, alpha=0.8)
    
    # Set viewing angle (rotating)
    ax.view_init(elev=25, azim=frame * 2)
    
    # Set limits and remove axes
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-3, 3)
    ax.axis('off')
    ax.set_box_aspect([1,1,0.8])
    
    # Remove background
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

# Create animation
print("Generating animated manifold... This may take a minute.")
frames = 180  # Full rotation
ani = FuncAnimation(fig, create_manifold_with_geodesics, 
                   frames=frames, interval=50, repeat=True)

# Save as GIF
output_path = 'assets/images/manifold.gif'
print(f"Saving animation to {output_path}...")
ani.save(output_path, writer=PillowWriter(fps=20))
print("Done! Your manifold GIF is ready.")

plt.close()
