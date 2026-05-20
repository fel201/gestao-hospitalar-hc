# Interfaces e Integrações

## 1. Protótipos
* [Prototipação da linha do tempo do paciente](https://www.figma.com/make/f9gHlb6W4nD1YsP2dd991K/User-Journey-Mapping-Panel?fullscreen=1&t=gMW54aou6TeWuQfb-1&code-node-id=0-9)

## 2. Hardware
* Impressoras térmicas e leitores de código de barras.

## 3. Software
* Integração com AGHU. 

### [SCHEMA] Interface de Integração (TypeScript)
```typescript
interface IHospitalApi {
  getPatientData(id: string): Promise<PatientRecord>;
  syncProntuario(data: ProntuarioUpdate): Promise<SyncResponse>;
  checkLdapAuth(credentials: AuthInfo): Promise<AuthStatus>;
}
```
