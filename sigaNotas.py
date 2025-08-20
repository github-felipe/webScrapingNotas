from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class sigaScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.produtos = []
        self.driver.get('https://siga.cps.sp.gov.br/sigaaluno/applogin.aspx')
        print("🚀 Navegador Chrome inicializado em modo headless")
        self.driver.find_element(By.CLASS_NAME, 'uc_flex-c.uc_pointer.uc_p30').click()
        print("🖊️ Indo para a tela de login")

        email_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_box.send_keys(input('Insira o seu email: '))  # Adiciona o email ao campo

        submit_box =self.wait.until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        submit_box.click()

        pass_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))
        )
        pass_box.send_keys(input('Insira a sua senha: '))  # Adiciona a senha ao campo

        submit_box = self.wait.until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        submit_box.click()

        mfa = self.wait.until(
                EC.visibility_of_element_located((By.ID, 'idRichContext_DisplaySign'))
            ).text

        print(f'Por favor, insira no seu autenticador da microsoft o código {mfa}')

        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'uc_appfooter-button.uc_pointer'))
        ).click()  # vai para a aba "meu curso"

        print('✅ Login efetuado com sucesso!')

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@onclick, 'MEUCURSO:HISTORICOESCOLAR')]"))
        ).click()

        disciplinas = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "uc_appcard"))
        )

        print('⏳ Checando as disciplinas...')

        for disciplina in disciplinas:
            try:
                dados = disciplina.find_element(By.CLASS_NAME, 'uc_appcard-content')
                media = dados.find_element(By.CLASS_NAME, 'uc_flex-r.uc_flex-jcsb.uc_w100.uc_mb5')
                media = float(media.find_element(By.CLASS_NAME, 'uc_apptext').text.replace(',', '.'))

                if media >= 6:
                    dados = disciplina.find_element(By.CLASS_NAME, 'uc_appcard-titlecontainer')
                    materia = dados.find_element(By.CLASS_NAME, 'uc_appcard-title').text
                    historico.append([materia, media])
            except Exception:
                print(f'Erro na busca de dados: \n{Exception}')

    def mostra_historico(self, dados):
        soma = 0
        print(f'{"Históico escolar":^48}')
        print(f'|{"Disciplina":<41}|Nota|')
        for dado in dados:
            print(f'|{dado[0]:<41}|{dado[1]:<4}|')
            soma += dado[1]
        print(f'Média final: {soma/len(dados)}')


historico = []

if __name__ == "__main__":
    scraper = sigaScraper()
    scraper.mostra_historico(historico)
