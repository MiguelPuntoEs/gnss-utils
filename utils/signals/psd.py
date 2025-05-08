import numpy as np


def phi_BOCc(f: float | np.ndarray, f0: float, m: int, n: float) -> float | np.ndarray:
    """
    BOCc Power Spectral Density (PSD) function.
    The BOCc signal is defined as:
    .. math::
        \\phi_{BOCc}(f) = \\frac{4}{f_0 n} \\text{sinc}^2\\left(\\frac{f}{f_0 n}\\right) \\left(\\frac{\\sin\\left(\\frac{\\pi f}{4 f_0 m}\\right)}{\\cos\\left(\\frac{\\pi f}{2 f_0 m}\\right)}\\right)^2
    where :math:`f_0` is the chip rate, :math:`m` is the number of chips in the BOC signal, and :math:`n` is the number of chips in the BOCc signal.
    Args:
        f (float or np.ndarray): Frequency in Hz.
        f0 (float): Chip rate in Hz.
        m (int): Number of chips in the BOC signal.
        n (float): Number of chips in the BOCc signal.
    Returns:
        float or np.ndarray: Power Spectral Density (PSD) of the BOCc signal at frequency f.
    """ 
    if (2*m/n)%2 ==0:
        return 4/(f0*n)*np.sinc(f/(f0*n))**2*(np.sin(np.pi*f/(4*(f0*m)))**2/np.cos(np.pi*f/(2*(f0*m))))**2
    else:
        return n*f0*(2*np.cos(np.pi*f/(n*f0))*np.sin(np.pi*f/(4*m*f0))/(np.pi*f*np.cos(np.pi*f/(2*m*f0))))**2   
    

def phi_BOCs(f: float | np.ndarray, f0: float, m: int, n: float) -> float | np.ndarray:
    """
    BOCs Power Spectral Density (PSD) function.
    The BOCs signal is defined as:
    .. math::
        \\phi_{BOCs}(f) = \\frac{4}{f_0 n} \\text{sinc}^2\\left(\\frac{f}{f_0 n}\\right) \\left(\\frac{\\sin\\left(\\frac{\\pi f}{4 f_0 m}\\right)}{\\cos\\left(\\frac{\\pi f}{2 f_0 m}\\right)}\\right)^2
    where :math:`f_0` is the chip rate, :math:`m` is the number of chips in the BOC signal, and :math:`n` is the number of chips in the BOCs signal.
    Args:
        f (float or np.ndarray): Frequency in Hz.
        f0 (float): Chip rate in Hz.
        m (int): Number of chips in the BOC signal.
        n (float): Number of chips in the BOCs signal.
    Returns:
        float or np.ndarray: Power Spectral Density (PSD) of the BOCs signal at frequency f.
    """
    if(2*m/n)%2 ==0:
        return phi_BOCc(f, f0, m, n)/np.tan(np.pi*f/(4*(f0*m)))**2
    else:
        return f0*n*(np.cos(np.pi*f/(n*f0))*np.sin(np.pi*f/(2*m*f0))/(np.pi*f*np.cos(np.pi*f/(2*m*f0))))**2
    
    
def phi_BPSK(f: float | np.ndarray, f0: float, n: float) -> float | np.ndarray:
    """
    BPSK Power Spectral Density (PSD) function.
    The BPSK signal is defined as:
    .. math::
        \\phi_{BPSK}(f) = \\frac{1}{f_0 n} \\text{sinc}^2\\left(\\frac{f}{f_0 n}\\right)
    where :math:`f_0` is the chip rate, and :math:`n` is the number of chips in the BPSK signal.
    Args:
        f (float or np.ndarray): Frequency in Hz.
        f0 (float): Chip rate in Hz.
        n (float): Number of chips in the BPSK signal.
    Returns:
        float or np.ndarray: Power Spectral Density (PSD) of the BPSK signal at frequency f.
    """

    return 1/(f0*n)*np.sinc(f/(f0*n))**2

def phi_AltBOC(f: float |np.ndarray, f0: float, m: int, n: int) -> float | np.ndarray:
    """
    AltBOC (constant envelope) Power Spectral Density (PSD) function.
    The AltBOC signal is defined as:
    .. math::
        \\phi_{AltBOC}(f) = \\frac{4}{f_0 n} \\text{sinc}^2\\left(\\frac{f}{f_0 n}\\right) \\left(\\frac{\\sin\\left(\\frac{\\pi f}{4 f_0 m}\\right)}{\\cos\\left(\\frac{\\pi f}{2 f_0 m}\\right)}\\right)^2
    where :math:`f_0` is the chip rate, :math:`m` is the number of chips in the AltBOC signal, and :math:`n` is the number of chips in the AltBOC signal.
    Args:
        f (float or np.ndarray): Frequency in Hz.
        f0 (float): Chip rate in Hz.
        m (int): Number of chips in the AltBOC signal.
        n (int): Number of chips in the AltBOC signal.
    Returns:
        float or np.ndarray: Power Spectral Density (PSD) of the AltBOC signal at frequency f.
    """
    if np.mod(m, 2)==1:
        return 4*(f0*n)/(np.pi*f)**2*np.cos(np.pi*f/(f0*n))**2/np.cos(np.pi*f/(2*f0*m))**2*(np.cos(np.pi*f/(f*f0*m))**2-np.cos(np.pi*f/(2*f0*m))-2*np.cos(np.pi*f/(2*f0*m))*np.cos(np.pi*f/(4*f0*m))+2)
    else:
        return 4*(f0*n)/(np.pi*f)**2*np.sin(np.pi*f/(f0*n))**2/np.cos(np.pi*f/(2*f0*m))**2*(np.cos(np.pi*f/(f*f0*m))**2-np.cos(np.pi*f/(2*f0*m))-2*np.cos(np.pi*f/(2*f0*m))*np.cos(np.pi*f/(4*f0*m))+2)

def phi_Altboc(f: float | np.ndarray, f0: float, m: int, n: int) -> float | np.ndarray:
    """
    Altboc (non-costant envelope AltBOC) Power Spectral Density (PSD) function.
    The Altboc signal is defined as:
    .. math::
        \\phi_{Altboc}(f) = \\frac{8}{f_0 n} \\text{sinc}^2\\left(\\frac{f}{f_0 n}\\right) \\left(\\frac{\\sin\\left(\\frac{\\pi f}{4 f_0 m}\\right)}{\\cos\\left(\\frac{\\pi f}{2 f_0 m}\\right)}\\right)^2
    where :math:`f_0` is the chip rate, :math:`m` is the number of chips in the Altboc signal, and :math:`n` is the number of chips in the Altboc signal.
    Args:
        f (float or np.ndarray): Frequency in Hz.
        f0 (float): Chip rate in Hz.
        m (int): Number of chips in the Altboc signal.
        n (int): Number of chips in the Altboc signal.
    Returns:
        float or np.ndarray: Power Spectral Density (PSD) of the Altboc signal at frequency f.
    """
    return 8*f0*n*(np.cos(np.pi*f/(f0*n))/(np.pi*f*np.cos(np.pi*f/(2*f0*m))))**2*(1-np.cos(np.pi*f/(2*f0*m)))