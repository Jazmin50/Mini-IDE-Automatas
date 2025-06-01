//Dania Jazmin Martinez Benitez
// Variables globales
let analysisTimeout = null;
const ANALYSIS_DELAY = 500; // Medio segundo de espera

// Función para mostrar el estado de carga
function showLoading(type) {
    const resultBox = document.getElementById(`${type}-analysis`) || document.getElementById('tm-result');
    resultBox.style.display = 'block';
    resultBox.classList.add('active');
    resultBox.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>Analizando código...</p>
        </div>
    `;
}

// Función para mostrar mensajes de error
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'global-error';
    errorDiv.innerHTML = `
        <div class="error-content">
            <i class="fas fa-exclamation-circle"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(errorDiv);
    setTimeout(() => {
        errorDiv.classList.add('show');
        setTimeout(() => {
            errorDiv.classList.remove('show');
            setTimeout(() => errorDiv.remove(), 300);
        }, 3000);
    }, 100);
}

// Función para actualizar los números de línea
function updateLineNumbers() {
    const textarea = document.getElementById('code');
    const lineNumbers = document.getElementById('line-numbers');
    const lines = textarea.value.split('\n');
    const numbers = lines.map((_, i) => i + 1).join('\n');
    lineNumbers.textContent = numbers;
}

async function runAnalysis(type) {
    try {
        const code = document.getElementById('code').value;
        
        // Validación específica para la máquina de Turing
        if (type === 'turing' && !code.trim()) {
            const resultBox = document.getElementById('tm-result');
            resultBox.innerHTML = `
                <div class="card-header">
                    <h2><i class="fas fa-robot"></i> Máquina de Turing</h2>
                </div>
                <div class="card-body compact-error">
                    <div class="turing-result error-container">
                        <i class="fas fa-exclamation-triangle"></i> Error: La cadena no puede estar vacía. Por favor, ingrese una cadena de 0s y 1s.
                    </div>
                </div>`;
            resultBox.style.display = 'block';
            return;
        }
        
        if (!code.trim() && type !== 'turing') {
            return;
        }

        // Ocultar resultados anteriores
        document.querySelectorAll('.result-box').forEach(box => {
            box.style.display = 'none';
        });

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, mode: type })
        });

        if (!response.ok) {
            throw new Error('Error en el servidor');
        }

        const result = await response.json();
        const resultBox = document.getElementById(`${type === 'lexico' ? 'lexical' : type === 'sintactico' ? 'syntactic' : 'tm'}-${type === 'turing' ? 'result' : 'analysis'}`);

        // LÉXICO
        if (type === 'lexico') {
            resultBox.innerHTML = `
                <div class="card-header">
                    <h2><i class="fas fa-search"></i> Análisis Léxico</h2>
                </div>
                <div class="card-body">
                    <table id="token-table">
                        <thead>
                            <tr>
                                <th>Valor</th>
                                <th>Tipo</th>
                                <th>Línea</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${result.tokens.map(tok => 
                                `<tr>
                                    <td>${escapeHtml(tok.value)}</td>
                                    <td>${escapeHtml(tok.type)}</td>
                                    <td>${tok.line}</td>
                                </tr>`
                            ).join('')}
                        </tbody>
                    </table>
                    ${result.lex_errors.length ? `
                        <div class="error-container">
                            <strong><i class="fas fa-exclamation-triangle"></i> Errores léxicos:</strong>
                            <ul>
                                ${result.lex_errors.map(err => 
                                    `<li>Línea ${err.line}: símbolo no reconocido '${escapeHtml(err.value)}'</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>`;
        }

        // SINTÁCTICO
        if (type === 'sintactico') {
            resultBox.innerHTML = `
                <div class="card-header">
                    <h2><i class="fas fa-cubes"></i> Análisis Sintáctico</h2>
                </div>
                <div class="card-body">
                    <div class="parse-result ${result.parse_errors.length ? 'has-error' : 'success'}">
                        ${result.parse_result}
                    </div>
                    ${result.parse_errors.length ? `
                        <div class="error-container">
                            <strong><i class="fas fa-exclamation-triangle"></i> Errores sintácticos:</strong>
                            <ul>
                                ${result.parse_errors.map(err => 
                                    `<li>Línea ${err.line}: ${escapeHtml(err.error)}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>`;
        }

        // MÁQUINA DE TURING
        if (type === 'turing') {
            resultBox.innerHTML = `
                <div class="card-header">
                    <h2><i class="fas fa-robot"></i> Máquina de Turing</h2>
                </div>
                <div class="card-body">
                    <div class="turing-result">
                        ${result.tm_result}
                    </div>
                </div>`;
        }

        resultBox.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
    }
}

// Función para escapar HTML y prevenir XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Función para análisis en tiempo real
async function realTimeAnalysis() {
    const code = document.getElementById('code').value;
    if (!code.trim()) {
        document.querySelectorAll('.result-box').forEach(box => {
            box.style.display = 'none';
        });
        return;
    }

    
    if (/^\d/.test(code.trim())) {
        document.getElementById('syntactic-analysis').style.display = 'none';
        return;
    }

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, mode: 'sintactico' })
        });

        if (!response.ok) {
            throw new Error('Error en el servidor');
        }

        const result = await response.json();
        const resultBox = document.getElementById('syntactic-analysis');

        if (result.lex_errors.length > 0 || result.parse_errors.length > 0) {
            resultBox.style.display = 'block';
            resultBox.innerHTML = `
                <div class="card-body">
                    ${result.lex_errors.length ? `
                        <div class="error-container">
                            <strong><i class="fas fa-exclamation-triangle"></i> Errores léxicos:</strong>
                            <ul>
                                ${result.lex_errors.map(err => 
                                    `<li>${escapeHtml(err.error)}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    ${result.parse_errors.length ? `
                        <div class="error-container">
                            <strong><i class="fas fa-exclamation-triangle"></i> Errores sintácticos:</strong>
                            <ul>
                                ${result.parse_errors.map(err => 
                                    `<li>${escapeHtml(err.error)}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>`;
        } else {
            resultBox.style.display = 'none';
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

// Inicializar y configurar el editor
const codeArea = document.getElementById('code');


updateLineNumbers();

// Eventos del editor
codeArea.addEventListener('input', function() {
    updateLineNumbers();
    
    // Cancelar el temporizador anterior si existe
    if (analysisTimeout) {
        clearTimeout(analysisTimeout);
    }
    
    // Crear nuevo temporizador para el análisis
    analysisTimeout = setTimeout(realTimeAnalysis, ANALYSIS_DELAY);
});

codeArea.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const value = this.value;
        const before = value.substring(0, start);
        const after = value.substring(end);
        this.value = before + '\n' + after;
        this.selectionStart = this.selectionEnd = start + 1;
        updateLineNumbers();
    } else if (e.key === 'Tab') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 4;
        updateLineNumbers();
    }
});

codeArea.addEventListener('scroll', () => {
    document.getElementById('line-numbers').scrollTop = codeArea.scrollTop;
});

// Atajos de teclado
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        // Ctrl+Enter para ejecutar el análisis léxico
        runAnalysis('lexico');
    } else if (e.ctrlKey && e.shiftKey && e.key === 'Enter') {
        // Ctrl+Shift+Enter para ejecutar el análisis sintáctico
        runAnalysis('sintactico');
    }
});
