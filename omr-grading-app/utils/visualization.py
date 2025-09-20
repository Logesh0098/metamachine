
import matplotlib.pyplot as plt
import numpy as np

def create_score_chart(scores):
    """Create a bar chart of scores"""
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = np.arange(len(scores))
    bars = ax.bar(x_pos, scores, color='skyblue')
    
    # Color bars based on score
    for i, bar in enumerate(bars):
        if scores[i] >= 80:
            bar.set_color('green')
        elif scores[i] >= 60:
            bar.set_color('orange')
        else:
            bar.set_color('red')
    
    ax.set_xlabel('Exam')
    ax.set_ylabel('Score (%)')
    ax.set_title('Exam Scores')
    ax.set_ylim(0, 100)
    
    return fig
