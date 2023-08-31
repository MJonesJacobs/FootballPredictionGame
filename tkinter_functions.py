def clear_subframes(frame):
    """Clear all subframes of a frame."""
    subframes = frame.winfo_children()
    for subframe in subframes:
        subframe.destroy()

