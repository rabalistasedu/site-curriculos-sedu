"""
Widget visual para seleção de categoria no admin.
Renderiza as categorias como botões com ícone, agrupados por área —
idêntico à grade da página "Documentos Curriculares" do site.
"""
from django import forms
from django.utils.safestring import mark_safe


def _render_rich_text_editor(name, widget_id, value):
    """HTML/CSS/JS do editor de texto rico compartilhado (RichTextWidget,
    e também usado fora de formulários Django, ex.: Estrutura de Árvores).
    Barra: negrito, itálico, sublinhado, alinhamento, lista, cor do texto,
    cor de destaque (marca-texto), limpar formatação."""
    botoes = [
        ('bold', 'fa-bold', 'Negrito'),
        ('italic', 'fa-italic', 'Itálico'),
        ('underline', 'fa-underline', 'Sublinhado'),
        ('|', '', ''),
        ('justifyLeft', 'fa-align-left', 'Alinhar à esquerda'),
        ('justifyCenter', 'fa-align-center', 'Centralizar'),
        ('justifyRight', 'fa-align-right', 'Alinhar à direita'),
        ('|', '', ''),
        ('insertUnorderedList', 'fa-list-ul', 'Lista com marcadores'),
        ('removeFormat', 'fa-eraser', 'Limpar formatação'),
    ]
    botoes_html = []
    for cmd, icone, titulo in botoes:
        if cmd == '|':
            botoes_html.append('<span class="rte-sep"></span>')
        else:
            botoes_html.append(
                f'<button type="button" class="rte-btn" data-cmd="{cmd}" title="{titulo}">'
                f'<i class="fas {icone}"></i></button>'
            )

    return f'''
<div class="rte-wrap">
    <div class="rte-toolbar">
        {''.join(botoes_html)}
        <span class="rte-sep"></span>
        <label class="rte-color-btn" title="Cor do texto">
            <i class="fas fa-font"></i>
            <input type="color" data-cmd="foreColor" value="#1a1a2e">
        </label>
        <label class="rte-color-btn" title="Cor de destaque (marca-texto)">
            <i class="fas fa-highlighter"></i>
            <input type="color" data-cmd="hiliteColor" value="#fff59d">
        </label>
    </div>
    <div class="rte-editor" contenteditable="true">{value}</div>
    <textarea name="{name}" id="{widget_id}" class="rte-textarea">{value}</textarea>
</div>
<script>
(function() {{
    var textarea = document.getElementById('{widget_id}');
    var wrap = textarea.closest('.rte-wrap');
    var editor = wrap.querySelector('.rte-editor');

    editor.addEventListener('input', function() {{ textarea.value = editor.innerHTML; }});

    // Guarda a última seleção feita dentro do editor — necessária porque
    // abrir o seletor de cor nativo tira o foco do editor e a seleção
    // de texto se perderia antes de aplicar a cor.
    document.addEventListener('selectionchange', function() {{
        var sel = window.getSelection();
        if (sel.rangeCount > 0 && editor.contains(sel.anchorNode)) {{
            editor._savedRange = sel.getRangeAt(0).cloneRange();
        }}
    }});
    function restaurarSelecao() {{
        var sel = window.getSelection();
        sel.removeAllRanges();
        if (editor._savedRange) {{
            sel.addRange(editor._savedRange);
        }} else {{
            editor.focus();
        }}
    }}

    wrap.querySelectorAll('.rte-btn').forEach(function(btn) {{
        btn.addEventListener('mousedown', function(e) {{ e.preventDefault(); }});
        btn.addEventListener('click', function() {{
            document.execCommand(btn.dataset.cmd, false, null);
            textarea.value = editor.innerHTML;
            editor.focus();
        }});
    }});

    wrap.querySelectorAll('.rte-color-btn input[type=color]').forEach(function(inp) {{
        inp.addEventListener('input', function() {{
            restaurarSelecao();
            try {{
                document.execCommand(inp.dataset.cmd, false, inp.value);
            }} catch (err) {{
                document.execCommand('backColor', false, inp.value);
            }}
            textarea.value = editor.innerHTML;
        }});
    }});
}})();
</script>
'''


class CategoriaPicker(forms.Widget):
    """Grade de botões com ícone para escolher a área de publicação."""

    class Media:
        css = {'all': (
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
            'css/admin_picker.css',
        )}

    def __init__(self, include_home=False, *args, **kwargs):
        self.include_home = include_home  # True para Banner (pode ser home)
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        from .models import Categoria

        value_str = str(value) if value else ''
        parts = ['<div class="cp-wrap">']

        if self.include_home:
            sel = ' cp-selected' if not value_str else ''
            parts.append(
                f'<div class="cp-home-option">'
                f'<label class="cp-btn cp-btn-home{sel}">'
                f'<input type="radio" name="{name}" value=""'
                f'{"checked" if not value_str else ""}>'
                f'<span class="cp-icon"><i class="fas fa-house"></i></span>'
                f'<span class="cp-label">Página inicial</span>'
                f'</label>'
                f'<p class="cp-home-hint">O banner aparecerá no carrossel da home.</p>'
                f'</div>'
            )

        pais = Categoria.objects.filter(
            ativa=True, categoria_pai__isnull=True
        ).order_by('ordem')

        for pai in pais:
            subs = pai.subcategorias.filter(ativa=True).order_by('nome')

            pai_icone = pai.icone or 'fas fa-folder-open'
            parts.append(
                f'<div class="cp-group">'
                f'<div class="cp-group-label">'
                f'<i class="{pai_icone}"></i> {pai.nome}'
                f'</div>'
                f'<div class="cp-group-btns">'
            )

            if not subs.exists():
                is_sel = (value_str == str(pai.pk))
                sel_cls = ' cp-selected' if is_sel else ''
                chk = 'checked' if is_sel else ''
                parts.append(
                    f'<label class="cp-btn{sel_cls}">'
                    f'<input type="radio" name="{name}" value="{pai.pk}" {chk}>'
                    f'<span class="cp-icon"><i class="{pai_icone}"></i></span>'
                    f'<span class="cp-label">{pai.nome}</span>'
                    f'</label>'
                )

            for sub in subs:
                netos = sub.subcategorias.filter(ativa=True).order_by('nome')
                if netos.exists():
                    sub_icone = sub.icone_display
                    parts.append(
                        f'<div class="cp-subgroup">'
                        f'<div class="cp-subgroup-label">'
                        f'<i class="{sub_icone}"></i> {sub.nome}'
                        f'</div>'
                    )
                    for neto in netos:
                        is_sel = (value_str == str(neto.pk))
                        sel_cls = ' cp-selected' if is_sel else ''
                        chk = 'checked' if is_sel else ''
                        icone = neto.icone_display
                        parts.append(
                            f'<label class="cp-btn{sel_cls}">'
                            f'<input type="radio" name="{name}" value="{neto.pk}" {chk}>'
                            f'<span class="cp-icon"><i class="{icone}"></i></span>'
                            f'<span class="cp-label">{neto.nome}</span>'
                            f'</label>'
                        )
                    parts.append('</div>')
                else:
                    is_sel = (value_str == str(sub.pk))
                    sel_cls = ' cp-selected' if is_sel else ''
                    chk = 'checked' if is_sel else ''
                    icone = sub.icone_display
                    parts.append(
                        f'<label class="cp-btn{sel_cls}">'
                        f'<input type="radio" name="{name}" value="{sub.pk}" {chk}>'
                        f'<span class="cp-icon"><i class="{icone}"></i></span>'
                        f'<span class="cp-label">{sub.nome}</span>'
                        f'</label>'
                    )

            parts.append('</div></div>')

        parts.append(
            '<script>'
            'document.querySelectorAll(".cp-btn input[type=radio]").forEach(function(r){'
            '  r.addEventListener("change",function(){'
            '    var wrap=this.closest(".cp-wrap");'
            '    wrap.querySelectorAll(".cp-btn").forEach(function(b){b.classList.remove("cp-selected");});'
            '    this.closest(".cp-btn").classList.add("cp-selected");'
            '  });'
            '});'
            '</script>'
        )
        parts.append('</div>')
        return mark_safe('\n'.join(parts))

    def value_from_datadict(self, data, files, name):
        val = data.get(name, '')
        return val if val else None


class IconPicker(forms.Widget):
    """Grade visual de ícones para escolher o ícone de um card de conteúdo."""

    class Media:
        css = {'all': (
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
            'css/admin_picker.css',
        )}

    def render(self, name, value, attrs=None, renderer=None):
        from .models import ICONES_CRIATIVOS

        value_str = value or ''

        # Lista de ícones únicos, na ordem em que aparecem no mapa temático.
        icones_unicos = []
        vistos = set()
        for _, icone in ICONES_CRIATIVOS:
            if icone not in vistos:
                vistos.add(icone)
                icones_unicos.append(icone)

        parts = ['<div class="cp-wrap">']

        sel_auto = ' cp-selected' if not value_str else ''
        parts.append(
            f'<div class="cp-home-option">'
            f'<label class="cp-btn cp-btn-home{sel_auto}">'
            f'<input type="radio" name="{name}" value="" '
            f'{"checked" if not value_str else ""}>'
            f'<span class="cp-icon"><i class="fas fa-wand-magic-sparkles"></i></span>'
            f'<span class="cp-label">Automático</span>'
            f'</label>'
            f'<p class="cp-home-hint">O site escolhe um ícone com base no título e na categoria.</p>'
            f'</div>'
        )

        parts.append('<div class="cp-group-btns">')
        for icone in icones_unicos:
            is_sel = (value_str == icone)
            sel_cls = ' cp-selected' if is_sel else ''
            chk = 'checked' if is_sel else ''
            parts.append(
                f'<label class="cp-btn cp-btn-icon{sel_cls}">'
                f'<input type="radio" name="{name}" value="{icone}" {chk}>'
                f'<span class="cp-icon"><i class="{icone}"></i></span>'
                f'</label>'
            )
        parts.append('</div>')

        parts.append(
            '<script>'
            'document.querySelectorAll(".cp-btn input[type=radio]").forEach(function(r){'
            '  r.addEventListener("change",function(){'
            '    var wrap=this.closest(".cp-wrap");'
            '    wrap.querySelectorAll(".cp-btn").forEach(function(b){b.classList.remove("cp-selected");});'
            '    this.closest(".cp-btn").classList.add("cp-selected");'
            '  });'
            '});'
            '</script>'
        )
        parts.append('</div>')
        return mark_safe('\n'.join(parts))

    def value_from_datadict(self, data, files, name):
        val = data.get(name, '')
        return val if val else ''


class RichTextWidget(forms.Widget):
    """Editor de texto simples com barra de formatação completa (negrito,
    itálico, sublinhado, alinhamento, lista, cor do texto e destaque/marca-texto)
    — sem depender de bibliotecas externas. Colar de outra fonte preserva a
    formatação (comportamento padrão do navegador em contenteditable)."""

    class Media:
        css = {'all': (
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
            'css/admin_picker.css',
        )}

    def render(self, name, value, attrs=None, renderer=None):
        value = value or ''
        attrs = attrs or {}
        widget_id = attrs.get('id', f'id_{name}')
        return mark_safe(_render_rich_text_editor(name, widget_id, value))
