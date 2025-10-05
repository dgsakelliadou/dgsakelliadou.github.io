"""
Alternative: Generate a sphere with geodesic flow patterns
Similar to the bottom-left image in your reference
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 10), facecolor='white')
ax = fig.add_subplot(111, projection='3d', facecolor='white')

def create_sphere_with_flows(frame):
    """Create a sphere with swirling geodesic patterns"""
    ax.clear()
    
    # Create sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    U, V = np.meshgrid(u, v)
    
    R = 2
    X = R * np.sin(V) * np.cos(U)
    Y = R * np.sin(V) * np.sin(U)
    Z = R * np.cos(V)
    
    # Color gradient based on height
    colors = (Z + R) / (2 * R)
    
    # Plot sphere with gradient
    ax.plot_surface(X, Y, Z, facecolors=plt.cm.rainbow(colors),
                   alpha=0.7, linewidth=0, antialiased=True)
    
    # Add spiral geodesic patterns
    num_spirals = 8
    for i in range(num_spirals):
        theta = np.linspace(0, 6 * np.pi, 300)
        phase = frame * 0.05 + i * 2 * np.pi / num_spirals
        
        # Spiral on sphere
        u_spiral = theta + phase
        v_spiral = np.pi/2 + 0.4 * np.sin(theta * 2)
        
        X_spiral = R * np.sin(v_spiral) * np.cos(u_spiral)
        Y_spiral = R * np.sin(v_spiral) * np.sin(u_spiral)
        Z_spiral = R * np.cos(v_spiral)
        
        color = plt.cm.cool(i / num_spirals)
        ax.plot(X_spiral, Y_spiral, Z_spiral, color=color, 
               linewidth=2.5, alpha=0.9)
    
    # Add concentric circles
    for pole in [-1, 1]:
        for rad in [0.3, 0.6, 0.9, 1.2]:
            circle_theta = np.linspace(0, 2*np.pi, 100)
            circle_r = rad
            circle_z = pole * np.sqrt(max(0, R**2 - circle_r**2))
            X_circle = circle_r * np.cos(circle_theta)
            Y_circle = circle_r * np.sin(circle_theta)
            Z_circle = np.full_like(X_circle, circle_z)
            
            ax.plot(X_circle, Y_circle, Z_circle, 
                   color='navy', linewidth=1.5, alpha=0.7)
    
    ax.view_init(elev=20, azim=frame * 2)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.axis('off')
    ax.set_box_aspect([1,1,1])

print("Generating sphere with geodesic flows...")
ani = FuncAnimation(fig, create_sphere_with_flows, frames=180, interval=50)
ani.save('assets/images/manifold_sphere.gif', writer=PillowWriter(fps=20))
print("Done! Saved as manifold_sphere.gif")
plt.close()
