COLORS = {
    'primary': '#2C3E50',
    'secondary': '#3498DB',
    'success': '#27AE60',
    'danger': '#E74C3C',
    'warning': '#F39C12',
    'light': '#ECF0F1',
    'dark': '#34495E',
    'white': '#FFFFFF',
    'text': '#2C3E50'
}

FONTS = {
    'title': ('Helvetica', 18, 'bold'),
    'heading': ('Helvetica', 14, 'bold'),
    'normal': ('Helvetica', 11),
    'small': ('Helvetica', 9)
}

BUTTON_STYLE = {
    'font': FONTS['normal'],
    'bg': COLORS['secondary'],
    'fg': COLORS['white'],
    'activebackground': COLORS['primary'],
    'activeforeground': COLORS['white'],
    'relief': 'flat',
    'padx': 20,
    'pady': 8,
    'cursor': 'hand2'
}

BUTTON_SUCCESS = {
    **BUTTON_STYLE,
    'bg': COLORS['success']
}

BUTTON_DANGER = {
    **BUTTON_STYLE,
    'bg': COLORS['danger']
}

ENTRY_STYLE = {
    'font': FONTS['normal'],
    'relief': 'solid',
    'bd': 1
}

LABEL_STYLE = {
    'font': FONTS['normal'],
    'bg': COLORS['light'],
    'fg': COLORS['text']
}

FRAME_STYLE = {
    'bg': COLORS['light'],
    'relief': 'flat'
}

TITLE_STYLE = {
    'font': FONTS['title'],
    'bg': COLORS['primary'],
    'fg': COLORS['white'],
    'pady': 15
}
