// Usando jQuery para facilitar o controle da visibilidade

const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
const dateInit = document.getElementById("id_date_init"); // Data de início das faturas
document.addEventListener('DOMContentLoaded', function () {
    const value_initial = document.getElementById("id_paymentmethod_accounts_set-INITIAL_FORMS");
    const formCountElem = document.getElementById("id_paymentmethod_accounts_set-TOTAL_FORMS");//TOTAL FORMS
    const installmentRange = document.getElementById('installment_Range')
    const dateInitsemvalor = document.getElementById("id_date_init"); // Data de início das faturas
    const templatenone = document.getElementById('id_paymentmethod_accounts_set-0-DELETE')
    const formContainer = document.getElementById("payment-method-container");
    // (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)
    // rascunho 02
    // CODIGO A PARTIR DAQ
    // Obtém os elementos principais
    
    console.log('value initial: ' + value_initial.value)
    console.log('total forms: ' + formCountElem.value)

    let part = 2
    // let part = 0
    let table = null;
    const installments = document.getElementById('generate')//gerador de parcelas
    installments.addEventListener('click', () => {
        console.log('ate o momento foi clicado o botao de gerar as parcelas')
        table = document.getElementById('acc')
        for (let index = 0; index < part; index++) {           
            let template = document.getElementById('empty-payment-method-form');
            let clone = template.content.cloneNode(true);
            formContainer.appendChild(clone);
        }
    })
    installments.addEventListener('click', () => {
        // const itensPaymentMethodContainer = formContainer.querySelectorAll("item-form");
        const formContainer = document.getElementById("payment-method-container");

        const itensPaymentMethodContainer = formContainer.querySelectorAll("div.form-row");
        const installment_Range = parseInt(document.getElementById("installment_Range").value); // Intervalo entre faturas (em dias)
        const totalValue = parseFloat(document.getElementById("id_totalValue").value); // Valor de cada parcela
        const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
    

        // console.log("Tá clicado meu amigo")
        // console.log(itensPaymentMethodContainer)
        // console.log(itensPaymentMethodContainer.length)
        // console.log(typeof itensPaymentMethodContainer)
        // itensPaymentMethodContainer.forEach(item=>{
        //     console.log('removido')
        //     // formContainer.removeChild(item)
        //     // let parent_button_3 = button.parentElement.parentElement.querySelector('input[type="hidden"][name$="-DELETE"]')
        //     // parent_button_3.value = 'on'
        // })
        // console.log(typeof(numberOfInstallments))

        // console.log(numberOfInstallments)
        formCountElem.value = numberOfInstallments
        // console.log(formCountElem.value)
        // no caso, value_initial serve para o formulario de update, para nao apagar os pagamentos já cadastrados que vem para
        // edição
        if (templatenone && value_initial==0) {
            templatenone.remove()
        }
        // --------------------------------- //
        // Validações básicas
        // converter a data no formato js 
        const convertToDate = (dateStr) => { //#FIXME inportante
            const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
            return new Date(year, month - 1, day); // Mês no JavaScript é baseado em zero
        };
        const inputDate = dateInit.value.trim();
        // Converter a data inicial
        const startDate = convertToDate(inputDate);
        // Verifica se a data foi convertida corretamente
        if (isNaN(startDate.getTime())) {
            console.error('Data inválida');
            return;
        }
        // --------------------------------- //

        if (isNaN(numberOfInstallments) || isNaN(installment_Range)  || isNaN(startDate) || isNaN(totalValue)) { 
            alert("Por favor, preencha todos os campos corretamente. BY: kleitin");
            return;
        }
        let initial_step =1;
        // console.log('cheguei auqi')
        // console.log(numberOfInstallments)
        //apaga tudo de UPDATE(PAGAMENTOS)
        // ao clicar em gerar novamente, ele marcará  o campo DELETE,assim pagamentos antes cadastrados serão deletados ao serem enviados.
        if(value_initial.value != 0){
            instance_payments = value_initial.parentElement.querySelectorAll(".form-row table");

            instance_payments.forEach(instance=>{
                // console.log(instance)
            //    ao clicar em gerar novamente
            
                delete_payment = instance.querySelector('.form-row table tr td input[type="hidden"][name$="DELETE"]');
                if (delete_payment) {
                    delete_payment.value = "on";
                    // console.log("Valor alterado para:", delete_payment.value);
                } else {
                    console.error("Input hidden para DELETE não encontrado!");
                }
                
                instance.style.display = "none"; 
                initial_step = parseInt(value_initial.value);

                
            })
        }
        
        if (table != null || value_initial.value != 0) {
                for (let index = 1; index <= formCountElem.value; index++) {
                    let div = document.getElementById('del') ;
                    if (div != null) {
                        div.remove();
                    }
                }


            table = null;
            formCountElem.value = initial_step;
        }
        
        const valueOfinstallments = compair(numberOfInstallments, totalValue);
        let index_value = 0;     
        const emptyFormTemplate = document.getElementById('empty-payment-method-form');
        for (let index = parseInt(value_initial.value) + 1 ; index < parseInt(value_initial.value) + numberOfInstallments + 1 ; index++) {
            if (!emptyFormTemplate) {
                console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
                return;
            }
        let template = document.getElementById('empty-payment-method-form');
        let clone = template.content.cloneNode(true);
        let row = template.querySelector("#row-form");

        clone.querySelectorAll("input, select").forEach(async (input) => {
            input.name = input.name.replace("__prefix__", formCountElem.value);
            input.id = input.id.replace("__prefix__", formCountElem.value);
            // Preenche os valores iniciais nos campos do formulário

            // CALCULO DE DADAS DE VENCIMENTO
            if (input.name.includes("-expirationDate")) {
                // Calcula a data da parcela
                days = (parseInt(installmentRange.value,10))
                new_date = startDate.setDate(startDate.getDate() + days);
                final_date = new Date(new_date)
                input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
                // console.log(input.value)
                // CALCULO DE VALOR
            }else if (input.name.includes("-value")) {
                // Define o valor da parcela
                input.value = valueOfinstallments[index_value];
                //CALCULO DE DIAS
                }else if (input.name.includes("-days")) {
                    // Define os dias entre as parcelas
                    input.value = installment_Range*(index-value_initial.value);
                    
                }
                // Adiciona o formulário ao contêiner
                await formContainer.appendChild(clone);
            })
            index_value+=1;
            formCountElem.value = Number(formCountElem.value) + 1
        }
    })
})
// for (let index = parseInt(value_initial.value) + 1 ; index < parseInt(value_initial.value) + numberOfInstallments + 1 ; index++) {
//     if (!emptyFormTemplate) {
//         console.error("Template de formulário vazio (empty-payment-method-form) não encontrado!");
//         return;
//     }
    
//     const newForm = emptyFormTemplate.content.cloneNode(true);
    // Atualiza os campos do formulário clonado

//         newForm.querySelectorAll("input, select").forEach(async (input) => {
//             input.name = input.name.replace("__prefix__", formCountElem.value);
//             input.id = input.id.replace("__prefix__", formCountElem.value);
//             // Preenche os valores iniciais nos campos do formulário

//             // CALCULO DE DADAS DE VENCIMENTO
//             if (input.name.includes("-expirationDate")) {
//                 // Calcula a data da parcela
//                 days = (parseInt(installmentRange.value,10))
//                 new_date = startDate.setDate(startDate.getDate() + days);
//                 final_date = new Date(new_date)
//                 input.value = `${final_date.getDate().toString().padStart(2, '0')}/${(final_date.getMonth() + 1).toString().padStart(2, '0')}/${final_date.getFullYear()} `  
//                 // console.log(input.value)
//                 // CALCULO DE VALOR
//             }else if (input.name.includes("-value")) {
//                 // Define o valor da parcela
//                 input.value = valueOfinstallments[index_value];
//                 //CALCULO DE DIAS
//                 }else if (input.name.includes("-days")) {
//                     // Define os dias entre as parcelas
//                     input.value = installment_Range*(index-value_initial.value);
             
//                 }
//                 // Adiciona o formulário ao contêiner
//                 await formContainer.appendChild(newForm);
//             })
//             index_value+=1;
//             formCountElem.value = Number(formCountElem.value) + 1
//         }
//     table = 'null';
//     part = formCountElem

// })
// console.log(numberOfInstallments)
// formCountElem.value = numberOfInstallments
// console.log(formCountElem.value)

    function compair(numero_parcelas, valor_total){
        const array_valor_parcelas = [];
        let all_parcela = 0
        for (let index = 0; index <= numero_parcelas-1; index++) {
            let valor_parcela = (valor_total/numero_parcelas).toFixed(2)
             
            all_parcela = parseFloat(all_parcela) + parseFloat(valor_parcela)
            if(index===numero_parcelas-1){
                let ultima_parcela = parseFloat(valor_parcela) + (valor_total - all_parcela);
                array_valor_parcelas[index] = ultima_parcela.toFixed(2);
            }else {
                array_valor_parcelas[index] = valor_parcela;
            }
        }
        return array_valor_parcelas
        // const generate = document.getElementById('generate')
        // generate.addEventListener('click', ()=> {
        //     const numberOfInstallments = parseInt(document.getElementById("id_numberOfInstallments").value); // Número de parcelas
        //     console.log(typeof(numberOfInstallments))
        //     console.log(numberOfInstallments)
        //     formCountElem.value = numberOfInstallments
        //     console.log(formCountElem.value)
        // })
    
        // document.addEventListener('DOMContentLoaded', function () {
    
        //     let part = 2
        //     // let part = 0
        //     let table = null;
        //     const installments = document.getElementById('generate')//gerador de parcelas
        //     installments.addEventListener('click', () => {
        //         console.log('ate o momento foi clicado o botao de gerar as parcelas: FUNÇÃO NOVA')
        //         for (let index = 0; index < part; index++) {           
        //             parcela = document.createElement('tr')
        //             row = document.createElement('td')
        //             forma_pagamento = document.createElement('input')
        //             expirationDate = document.createElement('input')
        //             days = document.createElement('input')
        //             value = document.createElement('input')
                    
                    
        //         }
        //     })
        // })
    }
